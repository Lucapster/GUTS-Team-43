import pygame

screen = pygame.display.set_mode((640, 640)) 

def character_customization(screen):
    font = pygame.font.Font(None, 40)


    #initial setup
    stats = {"Health": 0, "Speed": 0, "Strength": 0}
    points = 10
    customizing = True

    while customizing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if points > 0:

                    if event.key == pygame.K_1:
                        stats["Health"] += 1
                        points -= 1

                    elif event.key == pygame.K_2:
                        stats["Speed"] += 1
                        points -= 1

                    elif event.key == pygame.K_3:
                        stats["Strength"] += 1
                        points -= 1
                    
                elif event.key == pygame.K_RETURN:
                    customizing = False
                    return stats
                

        screen.fill((25, 25, 25))

        y = 150

        title = font.render("Character Customization", True, (255, 255, 255))
        screen.blit(title, (140, 50))

        for stat, value in stats.items():
            text = font.render(f"{stat}: {value}", True, (255, 255, 255))
            screen.blit(text, (200, y))
            y += 50

        remaining = font.render(f"Points left: {points}", True, (255, 255, 0))
        screen.blit(remaining, (200, y + 20))

        info = font.render("Press 1, 2, 3 to add | Enter to start", True, (0, 255, 0))
        screen.blit(info, (100, 500))

        pygame.display.flip()