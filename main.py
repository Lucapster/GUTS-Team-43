import pygame

pygame.init()

screen = pygame.display.set_mode((640, 640)) 


x = 0
y = 0

# load grass background wallpaper
# background = pygame.image.load("Image/grass.png").convert()
# background = pygame.transform.scale(background, (640, 640))


# load minecraft zombie image
# zombie_pixel = pygame.image.load('Image/zombie-pixel.png').convert_alpha()
# zombie_pixel = pygame.transform.scale(zombie_pixel, (50, 64))

# load human steve image
human_pixel = pygame.image.load("Image/human.png").convert_alpha()
human_pixel = pygame.transform.scale(human_pixel, (50, 50))

class pixel_image: 
    def __init__(self, image_path, size, x, y):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        self.x = x
        self.y = y

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

background = pixel_image("Image/grass.png", (640, 640), 0, 0)
zombie = pixel_image("Image/zombie-pixel.png", (50, 64), x ,y)


running = True

# main loop
while running:

    screen.fill((0, 0, 0))
    background.draw(screen)
    zombie.draw(screen)
    zombie.move(0.05, 0.05)

    

    # screen.blit(background, (0, 0)) # load the background

    # screen.blit(zombie_pixel, (x, y)) 
    screen.blit(human_pixel, (x + 100, y + 100))

    x += 0.05
    y += 0.05


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()