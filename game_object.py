import pygame


screen = pygame.display.set_mode((640, 640)) 


x = 0
y = 0

class pixel_image: 
    def __init__(self, image_path, size, x, y):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        self.x = x
        self.y = y

    def draw(self, screen = screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

background = pixel_image("Image/grass.png", (640, 640), 0, 0)
zombie = pixel_image("Image/zombie-pixel.png", (40, 64), x ,y)
human = pixel_image("Image/human.png", (50, 50),x, y)
apartment = pixel_image("Image/apartment.png", (130, 130), 100, 100)
shop = pixel_image("Image/shop.png", (100, 100), 100, 400)
concrete_background = pixel_image("Image/concrete.png", (1920, 1080), 0, 0)

human_poster = pixel_image("Image/human.png", (200, 200),10, 150)