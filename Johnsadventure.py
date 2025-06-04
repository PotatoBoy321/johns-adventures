import pygame
import sys
import time

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


# Load player sprites / assets
#Player idle sprites
player_img = pygame.image.load("SpriteFolder\Boy with Slingshot\Idle\idle1.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (50, 50))
player_img2 = pygame.image.load("SpriteFolder\Boy with Slingshot\Idle\idle2.png").convert_alpha()
player_img2 = pygame.transform.scale(player_img, (50, 50))  # Optional resize
player_img3 = pygame.image.load("SpriteFolder\Boy with Slingshot\Idle\idle3.png").convert_alpha()
player_img3 = pygame.transform.scale(player_img, (50, 50))  # Optional resize   
player_img4 = pygame.image.load("SpriteFolder\Boy with Slingshot\Idle\idle4.png").convert_alpha()
player_img4 = pygame.transform.scale(player_img, (50, 50))  # Optional resize

#Player walk sprites
player_img_walk = pygame.image.load("SpriteFolder\Boy with Slingshot\Walk\Walk1.png").convert_alpha()
player_img_walk = pygame.transform.scale(player_img_walk, (50, 50))  # Optional resize
Player_img_walk2 = pygame.image.load("SpriteFolder\Boy with Slingshot\Walk\Walk2.png").convert_alpha()
player_img_walk2 = pygame.transform.scale(Player_img_walk2, (50, 50))  # Optional resize
player_img_walk3 = pygame.image.load("SpriteFolder\Boy with Slingshot\Walk\Walk3.png").convert_alpha()
player_img_walk3 = pygame.transform.scale(player_img_walk3, (50, 50))  # Optional resize
player_img_walk4 = pygame.image.load("SpriteFolder\Boy with Slingshot\Walk\Walk4.png").convert_alpha()
player_img_walk4 = pygame.transform.scale(player_img_walk4, (50, 50))  # Optional resize

# Player jump sprite
player_img_jump = pygame.image.load("SpriteFolder\Boy with Slingshot\Jump\Jump without attack.png").convert_alpha()
player_img_jump = pygame.transform.scale(player_img_jump, (50, 50))  # Optional resize


#Player attack sprites
player_img_attack = pygame.image.load("SpriteFolder\Boy with Slingshot\Stay Attack\StayAttack1.png").convert_alpha()
player_img_attack = pygame.transform.scale(player_img_attack, (50, 50))
player_img_attack2 = pygame.image.load("SpriteFolder\Boy with Slingshot\Stay Attack\StayAttack2.png").convert_alpha() 
player_img_attack2 = pygame.transform.scale(player_img_attack2, (50, 50))
player_img_attack3 = pygame.image.load("SpriteFolder\Boy with Slingshot\Stay Attack\StayAttack3.png").convert_alpha()
player_img_attack3 = pygame.transform.scale(player_img_attack2, (50, 50))
player_img_attack4 = pygame.image.load("SpriteFolder\Boy with Slingshot\Stay Attack\StayAttack4.png").convert_alpha()
player_img_attack4 = pygame.transform.scale(player_img_attack4, (50, 50))
# Sprite classd
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.walk_frames = [frame1, frame2, frame3]  # Load these first!
        self.image = self.walk_frames[0]
        self.rect = self.image.get_rect()
        self.frame_index = 0
        self.last_update = pygame.time.get_ticks()  # Set a starting point
        self.frame_rate = 100
       
        self.image = player_img  # Default image
        self.rect = self.image.get_rect(center=(200, 150))
        self.vel_y = 0
        self.on_ground = False
        self.attacking = False
        
    def update(self, keys):
        if keys[pygame.K_d]:
            self.image = player_img_walk
                
           
            self.rect.x += 5
        elif keys[pygame.K_a]:
            self.image = player_img_walk
            #time.sleep(0.1)
            self.image = player_img_walk2
            #time.sleep(0.1)
            self.image = player_img_walk3
            #time.sleep(0.1)
            self.image = player_img_walk4
            #time.sleep(0.1)
            self.rect.x -= 5

        else:
            self.image = player_img

        if keys[pygame.K_w] and self.on_ground:
            self.image = player_img_jump
            self.vel_y = jump_strength
            self.on_ground = False

        if self.attacking:
            print("Attack key has been pressed")
            self.image = player_img_attack
            self.attacking = False  # Reset after attack

        
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
        
                

# Player setup
player_rect = pygame.Rect(100, 500, 50, 50)
player_vel_y = 0
gravity = 1
jump_strength = -20
on_ground = False

player = Player()
all_sprites = pygame.sprite.Group(player)

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
    all_sprites.update(keys)

    #Attack key left click
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:  # Left click
            player.attacking = True
            
            
        
            

    # Draw everything
    screen.fill(WHITE)
    screen.blit(player.image, player.rect.topleft)
    for platform in platforms:
        pygame.draw.rect(screen, GREEN, platform)

    pygame.display.update()
    clock.tick(FPS)
