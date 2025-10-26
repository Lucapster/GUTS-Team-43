import pygame
import random
from character_customization import character_customization, zombie_customization
from game_object import background, zombie, human, apartment, shop, concrete_background, pixel_image

pygame.init()

# Get full screen size
window_size = pygame.display.Info()
screen_width, screen_height = window_size.current_w, window_size.current_h

screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

# Get customization results
player_stats = character_customization(screen)
zombie_stats = zombie_customization(screen)

print("Character stats:", player_stats)
print("Zombie stats:", zombie_stats)

# === Generate multiple objects ===

# Backgrounds
backgrounds = [concrete_background]

# Humans (1–10)
humans = []
num_humans = random.randint(1, 10)
for _ in range(num_humans):
    x = random.randint(0, screen_width - 50)
    y = random.randint(0, screen_height - 50)
    humans.append(pixel_image("Image/human.png", (50, 50), x, y))

# Zombies (1–10)
zombies = []
num_zombies = random.randint(1, 10)
for _ in range(num_zombies):
    x = random.randint(0, screen_width - 64)
    y = random.randint(0, screen_height - 64)
    zombies.append(pixel_image("Image/zombie-pixel.png", (50, 64), x, y))

# Apartments (1–5)
apartments = []
num_apartments = random.randint(1, 5)
for _ in range(num_apartments):
    x = random.randint(0, screen_width - 130)
    y = random.randint(0, screen_height - 130)
    apartments.append(pixel_image("Image/apartment.png", (130, 130), x, y))

# Shops (1–5)
shops = []
num_shops = random.randint(1, 5)
for _ in range(num_shops):
    x = random.randint(0, screen_width - 100)
    y = random.randint(0, screen_height - 100)
    shops.append(pixel_image("Image/shop.png", (100, 100), x, y))

print(f"Generated {num_humans} humans, {num_zombies} zombies, {num_apartments} apartments, {num_shops} shops.")

# === Main Loop ===
running = True
clock = pygame.time.Clock()

while running:
    screen.fill((0, 0, 0))

    # Draw background
    for bg in backgrounds:
        bg.draw()

    # Draw static buildings
    for building in apartments + shops:
        building.draw()

    # Move & draw humans
    for h in humans:
        dx = random.uniform(-5, 5)
        dy = random.uniform(-1, 1)
        h.move(dx, dy)
        h.draw()


    # Move & draw zombies
    for z in zombies:
        z.move(0.05, 0.05)
        z.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(60)  # limit to 60 FPS

pygame.quit()
