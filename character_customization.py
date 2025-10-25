import pygame
from game_object import human_poster

screen = pygame.display.set_mode((640, 640)) 

def character_customization(screen):
    font = pygame.font.Font(None, 40)


    #initial setup
    stats = {"HP": 0, "Stamina" : 0, "Speed": 0, "Awareness_radius": 0}
    points = 10
    customizing = True

    buttons = {}
    y_start = 180
    for stat in stats:
        buttons[stat] = {
            "plus": pygame.Rect(400, y_start, 40, 40),
            "minus": pygame.Rect(460, y_start, 40, 40)
        }

        start_button = pygame.Rect(250, 550, 140, 50)

        y_start += 70


    while customizing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    customizing = False
                    return stats
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                
                
                mx, my = pygame.mouse.get_pos()

                if start_button.collidepoint(mx, my):
                    customizing = False
                    return stats

                for stat in stats:
                    if buttons[stat]["plus"].collidepoint(mx, my) and points > 0:
                        stats[stat] += 1
                        points -= 1
                    elif buttons[stat]["minus"].collidepoint(mx, my) and stats[stat] > 0:
                        stats[stat] -= 1
                        points += 1
                

        screen.fill((25, 25, 25))

        y = 150

        title = font.render("Character Customization", True, (255, 255, 255))
        screen.blit(title, (140, 50))


        # print the stats (eg: strength, speed, health) and its value 
        for stat, value in stats.items():
            text = font.render(f"{stat}: {value}", True, (255, 255, 255))
            screen.blit(text, (300, y))
            pygame.draw.rect(screen, (0, 200, 0), buttons[stat]["plus"])
            pygame.draw.rect(screen, (0, 200, 0), buttons[stat]["minus"])
            plus_text = font.render("+", True, (255,255,255))
            minus_text = font.render("-", True, (255,255,255))
            screen.blit(plus_text, (buttons[stat]["plus"].x + 10, buttons[stat]["plus"].y))
            screen.blit(minus_text, (buttons[stat]["minus"].x + 10, buttons[stat]["minus"].y))
        
            y += 70 

        remaining = font.render(f"Points left: {points}", True, (255, 255, 0))
        screen.blit(remaining, (300, y + 20))

        # trying to make the start button
        pygame.draw.rect(screen, (120, 61, 34), start_button, border_radius=8)
        start_text = font.render("Start", True, (255, 255, 255))
        text_rect = start_text.get_rect(center=start_button.center)
        screen.blit(start_text, text_rect)

        human_poster.draw()

        pygame.display.flip()