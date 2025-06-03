import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mario Platformer")

# Clock
clock = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Load player sprite
player_img = pygame.image.load("SpriteFolder/Boy with Slingshot/Idle/idle1.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (50, 50))  # Optional resize


# Player setup
player_rect = pygame.Rect(100, 500, 50, 50)
player_vel_y = 0
gravity = 1
jump_strength = -20
on_ground = False

# Platforms
platforms = [pygame.Rect(0, 550, 800, 50), pygame.Rect(300, 400, 200, 20)]

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_rect.x -= 5
    if keys[pygame.K_RIGHT]:
        player_rect.x += 5
    if keys[pygame.K_SPACE] and on_ground:
        player_vel_y = jump_strength
        on_ground = False

    # Gravity
    player_vel_y += gravity
    player_rect.y += player_vel_y

    # Collision with platforms
    on_ground = False
    for platform in platforms:
        if player_rect.colliderect(platform) and player_vel_y > 0:
            player_rect.y = platform.y - player_rect.height
            player_vel_y = 0
            on_ground = True

    # Draw everything
    screen.fill(WHITE)
    screen.blit(player_img, player_rect.topleft)
    for platform in platforms:
        pygame.draw.rect(screen, GREEN, platform)

    pygame.display.update()
    clock.tick(FPS)
