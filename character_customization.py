import pygame
from game_object import human_poster

screen = pygame.display.set_mode((640, 640)) 

def character_customization(screen):
    font = pygame.font.Font(None, 40)
    input_font = pygame.font.Font(None, 36)

    # Initial setup
    stats = {"HP": 0, "Stamina": 0, "Speed": 0, "Awareness_radius": 0}
    points = 10
    customizing = True

    # Stat buttons
    buttons = {}
    y_start = 180
    for stat in stats:
        buttons[stat] = {
            "plus": pygame.Rect(400, y_start, 40, 40),
            "minus": pygame.Rect(460, y_start, 40, 40)
        }
        y_start += 70

    # Input boxes for grid size
    input_boxes = {
        "x_grid": pygame.Rect(250, 450, 100, 40),
        "y_grid": pygame.Rect(420, 450, 100, 40)
    }
    inputs = {"x_grid": "", "y_grid": ""}
    active_box = None

    # Start button
    start_button = pygame.Rect(250, 550, 140, 50)

    while customizing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                # Check if clicked in input boxes
                active_box = None
                for key, box in input_boxes.items():
                    if box.collidepoint(mx, my):
                        active_box = key

                # Start button
                if start_button.collidepoint(mx, my):
                    if inputs["x_grid"].isdigit() and inputs["y_grid"].isdigit():
                        return stats, (int(inputs["x_grid"]), int(inputs["y_grid"]))
                    else:
                        print("Please enter valid grid sizes before starting.")

                # Stat buttons
                for stat in stats:
                    if buttons[stat]["plus"].collidepoint(mx, my) and points > 0:
                        stats[stat] += 1
                        points -= 1
                    elif buttons[stat]["minus"].collidepoint(mx, my) and stats[stat] > 0:
                        stats[stat] -= 1
                        points += 1

            elif event.type == pygame.KEYDOWN:
                # Handle typing for grid size input
                if active_box:
                    if event.key == pygame.K_BACKSPACE:
                        inputs[active_box] = inputs[active_box][:-1]
                    elif event.unicode.isdigit() and len(inputs[active_box]) < 3:
                        inputs[active_box] += event.unicode

                # Optional shortcut: Enter to confirm
                elif event.key == pygame.K_RETURN:
                    customizing = False

        # === Drawing ===
        screen.fill((25, 25, 25))

        title = font.render("Customize your character", True, (255, 255, 255))
        screen.blit(title, (140, 50))

        y = 150
        for stat, value in stats.items():
            text = font.render(f"{stat}: {value}", True, (255, 255, 255))
            screen.blit(text, (300, y))
            pygame.draw.rect(screen, (0, 200, 0), buttons[stat]["plus"])
            pygame.draw.rect(screen, (200, 0, 0), buttons[stat]["minus"])
            plus_text = font.render("+", True, (255,255,255))
            minus_text = font.render("-", True, (255,255,255))
            screen.blit(plus_text, (buttons[stat]["plus"].x + 10, buttons[stat]["plus"].y))
            screen.blit(minus_text, (buttons[stat]["minus"].x + 10, buttons[stat]["minus"].y))
            y += 70 

        remaining = font.render(f"Points left: {points}", True, (255, 255, 0))
        screen.blit(remaining, (300, y + 75))

        # Grid input section
        grid_label = font.render("Map Grid Size:", True, (255, 255, 255))
        screen.blit(grid_label, (10, 455))

        x_label = input_font.render("X:", True, (255, 255, 255))
        y_label = input_font.render("Y:", True, (255, 255, 255))
        screen.blit(x_label, (220, 455))
        screen.blit(y_label, (390, 455))

        for key, box in input_boxes.items():
            color = (0, 200, 0) if active_box == key else (150, 150, 150)
            pygame.draw.rect(screen, color, box, 2)
            text_surface = input_font.render(inputs[key], True, (255, 255, 255))
            screen.blit(text_surface, (box.x + 10, box.y + 5))

        # Start button
        pygame.draw.rect(screen, (120, 61, 34), start_button, border_radius=8)
        start_text = font.render("Start", True, (255, 255, 255))
        text_rect = start_text.get_rect(center=start_button.center)
        screen.blit(start_text, text_rect)

        # Human poster
        human_poster.draw()

        pygame.display.flip()
