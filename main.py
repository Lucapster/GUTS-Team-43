import pygame
from game_obejct import background, zombie, human, apartment, shop

pygame.init()

screen = pygame.display.set_mode((640, 640)) 
  
x = 0
y = 0

running = True

# main loop
while running:

    screen.fill((0, 0, 0))
    background.draw()
    apartment.draw()
    shop.draw()
    

    zombie.draw()
    human.draw()
    

    human.move(0.1, 0.1)
    zombie.move(0.05, 0.05)

    x += 0.05
    y += 0.05


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()