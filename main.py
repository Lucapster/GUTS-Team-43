import pygame
from character_customization import character_customization
from game_object import background, zombie, human, apartment, shop

pygame.init()

window_size = pygame.display.Info()
screen_width, screen_height = window_size.current_w, window_size.current_h

screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE) 

player_stats = character_customization(screen)
print("Chosen stats:", player_stats)
  
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