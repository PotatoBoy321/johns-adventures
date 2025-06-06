import pygame
import sys
import random
import os

pygame.init()
pygame.mixer.init()

# ——— MUSIC ———
pygame.mixer.music.load("SlaveQ_Dr_Dre_style_-_SlaveQ.mp3")
pygame.mixer.music.play(-1)

# ——— SCREEN ———
WIDTH, HEIGHT = 800, 600
WORLD_WIDTH = 25000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Side Scroller with Waves (Cheats & Restart)")

clock = pygame.time.Clock()
FPS = 60

# ——— COLORS ———
WHITE     = (255, 255, 255)
GRAY      = (100, 100, 100)
DARK_GRAY = (60, 60, 60)
YELLOW    = (255, 255, 0)
RED       = (200, 0, 0)

# ——— BACKGROUND LOAD ———
background_path = "C:/Users/uaa_coenglab209login/Documents/awnflawdfnpaw/EX/SpriteFolder/bg.png"
if not os.path.isfile(background_path):
    raise FileNotFoundError(f"Background image not found: {background_path}")
background_image = pygame.image.load(background_path).convert()
background_image = pygame.transform.scale(background_image, (WORLD_WIDTH, HEIGHT))

# ——— MOB IMAGE ———
mob_path = "C:/Users/uaa_coenglab209login/Documents/awnflawdfnpaw/EX/Transparent PNG/1.png"
if not os.path.isfile(mob_path):
    raise FileNotFoundError(f"Mob image not found: {mob_path}")
mob_image = pygame.image.load(mob_path).convert_alpha()
mob_image = pygame.transform.scale(mob_image, (50, 50))

# ——— PLAYER ANIMATION LOADING ———
frame_delay = 8
animation = {
    "idle": [
        pygame.transform.scale(
            pygame.image.load(
                f"C:/Users/uaa_coenglab209login/Documents/awnflawdfnpaw/EX/SpriteFolder/Boy with Slingshot/Idle/idle{i}.png"
            ).convert_alpha(),
            (50, 50),
        )
        for i in range(1, 5)
    ],
    "walk": [
        pygame.transform.scale(
            pygame.image.load(
                f"C:/Users/uaa_coenglab209login/Documents/awnflawdfnpaw/EX/SpriteFolder/Boy with Slingshot/Walk/Walk{i}.png"
            ).convert_alpha(),
            (50, 50),
        )
        for i in range(1, 5)
    ],
    "jump": [
        pygame.transform.scale(
            pygame.image.load(
                "C:/Users/uaa_coenglab209login/Documents/awnflawdfnpaw/EX/SpriteFolder/Boy with Slingshot/Jump/Jump without attack.png"
            ).convert_alpha(),
            (50, 50),
        )
    ],
    "attack": [
        pygame.transform.scale(
            pygame.image.load(
                f"C:/Users/uaa_coenglab209login/Documents/awnflawdfnpaw/EX/SpriteFolder/Boy with Slingshot/Stay Attack/StayAttack{i}.png"
            ).convert_alpha(),
            (50, 50),
        )
        for i in range(1, 5)
    ],
}

# ——— PLATFORMS ———
platforms = [pygame.Rect(0, 550, WORLD_WIDTH, 50)]
for _ in range(130):
    x = random.randint(0, WORLD_WIDTH - 120)
    y = random.randint(150, 500)
    platforms.append(pygame.Rect(x, y, random.randint(80, 160), 20))

# ——— FONTS ———
ui_font    = pygame.font.SysFont(None, 24)
death_font = pygame.font.SysFont(None, 48)

# ——— PLAYER CLASS ———
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.action = "idle"
        self.frame_index = 0
        self.frame_timer = 0
        self.image = animation[self.action][self.frame_index]
        self.rect = self.image.get_rect(center=(200, 400))
        self.vel_y = 0
        self.on_ground = False
        self.attacking = False
        self.facing_right = True
        self.alive = True

    def update(self, keys):
        if not self.alive:
            return

        prev_action = self.action
        dx = 0

        if keys[pygame.K_a]:
            dx = -5
            self.facing_right = False
        if keys[pygame.K_d]:
            dx = 5
            self.facing_right = True

        if keys[pygame.K_w] and self.on_ground:
            self.vel_y = jump_strength
            self.on_ground = False

        if self.attacking:
            self.action = "attack"
        elif not self.on_ground:
            self.action = "jump"
        elif dx != 0:
            self.action = "walk"
        else:
            self.action = "idle"

        self.rect.x += dx
        self.vel_y += gravity
        self.rect.y += self.vel_y

        # Clamp within world bounds
        self.rect.x = max(0, min(WORLD_WIDTH - self.rect.width, self.rect.x))

        # Platform collision
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform) and self.vel_y > 0:
                self.rect.bottom = platform.top
                self.vel_y = 0
                self.on_ground = True

        # Advance animation frames
        self.frame_timer += 1
        if self.frame_timer >= frame_delay:
            self.frame_timer = 0
            self.frame_index = (self.frame_index + 1) % len(animation[self.action])
            if self.action == "attack" and self.frame_index == 0:
                self.attacking = False

        if self.action != prev_action:
            self.frame_index = 0

        self.image = animation[self.action][self.frame_index]


# ——— MOB CLASS ———
class Mob:
    def __init__(self, x, y, mob_type="normal"):
        self.type = mob_type
        size = 50 if mob_type == "tank" else 40
        self.image = pygame.transform.scale(mob_image.copy(), (size, size))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel_y = 0

        if mob_type == "fast":
            self.speed = 4
            self.health = 1
        elif mob_type == "tank":
            self.speed = 1
            self.health = 5
        else:
            self.speed = 2
            self.health = 2

    def update(self):
        # Move toward player
        if player.rect.centerx > self.rect.centerx:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

        # Apply gravity
        self.vel_y += gravity
        self.rect.y += self.vel_y

        # Platform collision
        for plat in platforms:
            if self.rect.colliderect(plat) and self.vel_y > 0:
                self.rect.bottom = plat.top
                self.vel_y = 0
                break

    def draw(self, offset_x):
        screen.blit(self.image, (self.rect.x - offset_x, self.rect.y))


# ——— WAVE SPAWNING & DRAW FUNCTION ———
def spawn_wave(wave_num):
    wave_list = []
    mob_count = 3 + wave_num * 2
    for _ in range(mob_count):
        x = random.randint(player.rect.x + 600, player.rect.x + 1800)
        y = 0
        mob_type = random.choices(["fast", "normal", "tank"], weights=[0.3, 0.5, 0.2])[0]
        wave_list.append(Mob(x, y, mob_type))
    return wave_list


def draw_world(offset_x, mobs, wave_num):
    screen.blit(background_image, (-offset_x, 0))

    # Draw platforms
    for plat in platforms:
        pygame.draw.rect(
            screen,
            GRAY,
            pygame.Rect(plat.x - offset_x, plat.y, plat.width, plat.height),
        )

    # Draw bullets
    for bullet in bullets:
        pygame.draw.rect(
            screen,
            YELLOW,
            pygame.Rect(
                bullet["rect"].x - offset_x,
                bullet["rect"].y,
                bullet["rect"].width,
                bullet["rect"].height,
            ),
        )

    # Draw mobs
    for m in mobs:
        m.draw(offset_x)

    # Draw player only if alive
    if player.alive:
        screen.blit(player.image, (player.rect.x - offset_x, player.rect.y))

    # Draw wave UI (dark bar + text)
    pygame.draw.rect(screen, DARK_GRAY, (10, 10, 150, 30))
    wave_text = ui_font.render(f"Wave: {wave_num}", True, WHITE)
    screen.blit(wave_text, (20, 12))


# ——— MAIN GAME SETUP ———
gravity = 1
jump_strength = -20
player = Player()
all_sprites = pygame.sprite.Group(player)

bullets = []
bullet_speed = 10
shoot_cooldown = 300
last_shot_time = 0

wave = 1
mobs = spawn_wave(wave)

# ——— MAIN LOOP ———
running = True
while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # — SHOOTING —
        elif player.alive and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            now = pygame.time.get_ticks()
            if now - last_shot_time > shoot_cooldown:
                player.attacking = True
                direction = 1 if player.facing_right else -1
                bullet_rect = pygame.Rect(
                    player.rect.centerx, player.rect.centery, 10, 4
                )
                bullets.append({"rect": bullet_rect, "speed": bullet_speed * direction})
                last_shot_time = now

        # — CHEAT: skip to next wave with N key —
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_n:
            if player.alive:
                mobs.clear()  # clear current wave
                wave += 1
                mobs = spawn_wave(wave)

        # — RESTART: press R when dead —
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            if not player.alive:
                # Reset game state
                player = Player()
                all_sprites = pygame.sprite.Group(player)
                bullets.clear()
                wave = 1
                mobs = spawn_wave(wave)

    # Update player if alive
    if player.alive:
        player.update(keys)

    # Update bullets
    for bullet in bullets[:]:
        bullet["rect"].x += bullet["speed"]
        # Remove if offscreen
        if bullet["rect"].right < 0 or bullet["rect"].left > WORLD_WIDTH:
            bullets.remove(bullet)
        else:
            # Check bullet vs. mob collision
            for m in mobs[:]:
                if bullet["rect"].colliderect(m.rect):
                    m.health -= 1
                    bullets.remove(bullet)
                    if m.health <= 0:
                        mobs.remove(m)
                    break

    # Update mobs & check collision with player
    for m in mobs:
        m.update()
        if player.alive and player.rect.colliderect(m.rect):
            player.alive = False

    # Next wave if all mobs are gone
    if player.alive and not mobs:
        wave += 1
        mobs = spawn_wave(wave)

    # Camera follows player
    camera_offset = player.rect.centerx - (WIDTH // 2)
    camera_offset = max(0, min(camera_offset, WORLD_WIDTH - WIDTH))

    # Draw everything
    screen.fill(WHITE)
    draw_world(camera_offset, mobs, wave)

    # If player died, show funny death message + “Press R to restart”
    if not player.alive:
        death_surf = death_font.render("Uh‑oh, you got pixel‑pummeled!", True, RED)
        death_rect = death_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
        screen.blit(death_surf, death_rect)

        restart_surf = ui_font.render("Press R to restart", True, RED)
        restart_rect = restart_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
        screen.blit(restart_surf, restart_rect)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()
