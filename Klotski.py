import pygame

pygame.init()

class Block(object):
    moved = False
    displace_x = 0
    displace_y = 0

    def __init__(self, x, y, x_area, y_area, id, type):
        self.rect = pygame.Rect(x, y, x_area, y_area)
        self.id = id
        self.type = type
    def move(self, x, y):
        collision_walls = self.rect.move(x,y).collidelist(walls)
        collision_rects = self.rect.move(x,y).collidelist([e.rect for e in blocks if e is not self])
        if collision_walls < 0 and collision_rects < 0:
            self.rect = self.rect.move(x,y)
            self.moved = True
            self.displace_x += x
            self.displace_y += y

screen_size = pygame.display.Info()
wall_size = (screen_size.current_h * 9 / 10) / 37
board_height = wall_size * 37
block_size = wall_size * 7
board_width = wall_size * 30
screen = pygame.display.set_mode((board_width, board_height))

# RGB tuples for color
black = (0, 0, 0)
green = (0, 255, 0)
seashell = (255, 245, 238)
darkblue = (72, 61, 139)
lavender = (230, 230, 250)
gold = (255, 215, 0)

# Font for text
myfont = pygame.font.SysFont("times new roman", int(0.5 * block_size))

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Keeps track of moves made
moveCount = 0

# Sound
click = pygame.mixer.Sound("click.wav")

win_text = myfont.render("YOU WIN!", 1, green)

imageList = ["verticalcat1.png", "verticalcat2.png", "verticalcat3.png", "verticalcat4.png", "horizontalcat.png",\
             "squarecat1.png", "squarecat2.png", "squarecat3.png", "squarecat4.png", "cat.png"]
images = []

for img in imageList:
    images.append(pygame.image.load(img))

background_image = pygame.image.load("grass_texture_seamless.png")

block1 = Block(wall_size, wall_size, block_size, block_size * 2, "block1", "vert_block")
block2 = Block(block_size * 3 + wall_size, wall_size, block_size, block_size * 2, "block2", "vert_block")
block3 = Block(wall_size, block_size * 2 + wall_size, block_size, block_size * 2, "block3", "vert_block")
block4 = Block(block_size * 3 + wall_size, 2 * block_size + wall_size, block_size, block_size * 2, "block4",
               "vert_block")
block5 = Block(block_size + wall_size, block_size * 2 + wall_size, block_size * 2, block_size, "block5",
               "vert_block")
smallblock1 = Block(wall_size, 4 * block_size + wall_size, block_size, block_size, "smallblock1", "small_block")
smallblock2 = Block(block_size + wall_size, 3 * block_size + wall_size, block_size, block_size, "smallblock2",
                    "small_block")
smallblock3 = Block(2 * block_size + wall_size, 3 * block_size + wall_size, block_size, block_size,
                    "smallblock3", "small_block")
smallblock4 = Block(3 * block_size + wall_size, 4 * block_size + wall_size, block_size, block_size,
                    "smallblock4", "small_block")
center_block = Block(block_size + wall_size, wall_size, block_size * 2, block_size * 2, "center_block", "center_block")
walls = [pygame.Rect(0, 0, wall_size, board_height - wall_size), pygame.Rect(0, 0, board_width - wall_size, wall_size),
         pygame.Rect(board_width - wall_size, 0, wall_size, board_height - wall_size),
         pygame.Rect(0, board_height - wall_size, board_height, wall_size)]
blocks = [block1, block2, block3, block4, block5, smallblock1, smallblock2, smallblock3, smallblock4, center_block]

def select_block(mouse_pos, blocks):
    mouse_x = mouse_pos[0]
    mouse_y = mouse_pos[1]
    for e in blocks:
        if e.rect.left < mouse_x < e.rect.right and e.rect.bottom > mouse_y > e.rect.top:
            return e
    return 0

def draw_screen():
    background = pygame.transform.scale(background_image, (board_width, board_height))
    screen.blit(background, (0, 0))
    for e in walls:
        pygame.draw.rect(screen, darkblue, e)
    title_string = "Klotski - Total Moves: " + str(moveCount)
    pygame.display.set_caption(title_string)

    for img, blk in zip(images, blocks):
        new_img = pygame.transform.scale(img, (blk.rect.width, blk.rect.height))
        pygame.draw.rect(screen, gold, blk.rect)
        screen.blit(new_img, blk)

    pygame.display.flip()

last_block = 0
selected_block = 0
mouseHeldDown = False
blockMove = (0, 0)

tmp_x = 0
tmp_y = 0

# Decides when to shift block
threshold = block_size / 2

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseHeldDown = True
            selected_block = select_block(pygame.mouse.get_pos(), blocks)
            
            if selected_block in blocks:
                x_pos = selected_block.rect.x
                y_pos = selected_block.rect.y
                selected_block.displace_x = 0
                selected_block.displace_y = 0
            pygame.mouse.get_rel()
        elif event.type == pygame.MOUSEBUTTONUP:
            mouseHeldDown = False
            if selected_block in blocks:
                tmp_x = selected_block.displace_x % block_size
                if tmp_x > threshold:
                    selected_block.move(block_size - tmp_x, 0)
                else:
                    selected_block.move(-tmp_x, 0)

                tmp_y = selected_block.displace_y % block_size
                if tmp_y > threshold:
                    selected_block.move(0, block_size - tmp_y)
                else:
                    selected_block.move(0, -tmp_y)

                if selected_block.displace_x or selected_block.displace_y:
                    moveCount += 1
                    click.play()
                last_block = selected_block
            selected_block = 0
        elif mouseHeldDown:
            blockMove = pygame.mouse.get_rel()
            if selected_block in blocks:
                selected_block.move(blockMove[0], 0)
                selected_block.move(0, blockMove[1])
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                if moveCount > 0:
                    if last_block.rect.x != x_pos or last_block.rect.y != y_pos:
                        click.play()
                        last_block.rect.x = x_pos
                        last_block.rect.y = y_pos
                        moveCount -= 1
        elif center_block.rect.left == wall_size + block_size and \
            center_block.rect.bottom == board_height - wall_size:
            screen.fill(black)
            screen.blit(win_text, (wall_size + 0.9 * block_size, 2 * block_size + wall_size))
            pygame.display.flip()
            pygame.time.wait(10000)
            done = True
        draw_screen()
    clock.tick(60)
pygame.quit()
