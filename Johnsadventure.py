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

# Animation control
current_action = "idle"
frame_index = 0
frame_timer = 0
frame_delay = 8

# Load animation frames
animation = {
    "idle": [
        pygame.transform.scale(pygame.image.load(f"SpriteFolder/Boy with Slingshot/Idle/idle{i}.png").convert_alpha(), (50, 50))
        for i in range(1, 5)
    ],
    "walk": [
        pygame.transform.scale(pygame.image.load(f"SpriteFolder/Boy with Slingshot/Walk/Walk{i}.png").convert_alpha(), (50, 50))
        for i in range(1, 5)
    ],
    "jump": [
        pygame.transform.scale(pygame.image.load("SpriteFolder/Boy with Slingshot/Jump/Jump without attack.png").convert_alpha(), (50, 50))
    ],
    "attack": [
        pygame.transform.scale(pygame.image.load(f"SpriteFolder/Boy with Slingshot/Stay Attack/StayAttack{i}.png").convert_alpha(), (50, 50))
        for i in range(1, 5)
    ]
}

# Platforms
platforms = [pygame.Rect(0, 550, 800, 50), pygame.Rect(300, 400, 200, 20)]

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.action = "idle"
        self.frame_index = 0
        self.frame_timer = 0
        self.image = animation[self.action][self.frame_index]
        self.rect = self.image.get_rect(center=(200, 150))
        self.vel_y = 0
        self.on_ground = False
        self.attacking = False

    def update(self, keys):
        prev_action = self.action

        if keys[pygame.K_a]:
            self.rect.x -= 5
            self.action = "walk"
        elif keys[pygame.K_d]:
            self.rect.x += 5
            self.action = "walk"
        elif keys[pygame.K_w] and self.on_ground:
            self.vel_y = jump_strength
            self.on_ground = False
            self.action = "jump"
        elif self.attacking:
            self.action = "attack"
        else:
            self.action = "idle"

        # Gravity
        self.vel_y += gravity
        self.rect.y += self.vel_y

        # Collision
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform) and self.vel_y > 0:
                self.rect.bottom = platform.top
                self.vel_y = 0
                self.on_ground = True

        # Animation update
        self.frame_timer += 1
        if self.frame_timer >= frame_delay:
            self.frame_timer = 0
            self.frame_index += 1
            if self.frame_index >= len(animation[self.action]):
                self.frame_index = 0
                if self.action == "attack":
                    self.attacking = False

        # Only reset frame index when switching actions
        if self.action != prev_action:
            self.frame_index = 0

        self.image = animation[self.action][self.frame_index]

# Game values
gravity = 1
jump_strength = -20
player = Player()
all_sprites = pygame.sprite.Group(player)

# Game loop
running = True
while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                player.attacking = True

    # Update
    all_sprites.update(keys)

    # Draw
    screen.fill(WHITE)
    for platform in platforms:
        pygame.draw.rect(screen, GREEN, platform)
    all_sprites.draw(screen)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()
