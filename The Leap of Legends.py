import pygame
import sys
import os

pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer Game Demo")

# FPS
FPS = 60
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (100, 200, 100)
BLUE = (100, 100, 200)
RED = (200, 50, 50)
YELLOW = (255, 223, 0)
BROWN = (139, 69, 19)

# Fonts
FONT = pygame.font.SysFont("Arial", 24)
BIG_FONT = pygame.font.SysFont("Arial", 48)

# Player attributes
PLAYER_WIDTH, PLAYER_HEIGHT = 40, 60
PLAYER_SPEED = 5
PLAYER_JUMP_POWER = 20
GRAVITY = 1

# Enemy attributes
ENEMY_WIDTH, ENEMY_HEIGHT = 40, 60
ENEMY_SPEED = 2

# Coin attributes
COIN_SIZE = 20

# Lives
MAX_LIVES = 3

# Levels data
levels = [
    {
        "start_pos": (100, HEIGHT - 100),
        "platforms": [
            (0, HEIGHT - 40, WIDTH, 40),
            (200, 450, 100, 20),
            (400, 350, 100, 20),
            (600, 250, 100, 20),
        ],
        "enemies": [
            {"pos": (300, HEIGHT - 100), "range": (300, 500)},
            {"pos": (500, 430), "range": (400, 600)}
        ],
        "coins": [
            (220, 410), (420, 310), (620, 210)
        ]
    },
    {
        "start_pos": (100, HEIGHT - 100),
        "platforms": [
            (0, HEIGHT - 40, WIDTH, 40),
            (150, 500, 100, 20),
            (350, 400, 100, 20),
            (550, 300, 100, 20),
            (700, 200, 80, 20)
        ],
        "enemies": [
            {"pos": (250, 480), "range": (200, 300)},
            {"pos": (450, 380), "range": (400, 500)},
            {"pos": (650, 280), "range": (600, 700)},
        ],
        "coins": [
            (170, 460), (370, 360), (570, 260), (720, 160)
        ]
    },
    {
        "start_pos": (100, HEIGHT - 100),
        "platforms": [
            (0, HEIGHT - 40, WIDTH, 40),
            (250, 500, 100, 20),
            (450, 400, 100, 20),
            (650, 300, 100, 20),
        ],
        "enemies": [
            {"pos": (300, HEIGHT - 100), "range": (200, 400)},
            {"pos": (500, 380), "range": (450, 650)},
        ],
        "coins": [
            (270, 460), (470, 360), (670, 260)
        ]
    },
    {
        # Modified start_pos for level 4
        "start_pos": (50, HEIGHT - 100),
        "platforms": [
            (0, HEIGHT - 40, WIDTH, 40),
            (100, 500, 100, 20),
            (300, 450, 100, 20),
            (500, 350, 100, 20),
            (700, 250, 80, 20)
        ],
        "enemies": [
            {"pos": (120, 480), "range": (100, 200)},
            {"pos": (320, 430), "range": (300, 400)},
            {"pos": (520, 330), "range": (500, 600)},
        ],
        "coins": [
            (120, 460), (320, 410), (520, 310), (720, 210)
        ]
    },
    {
        "start_pos": (100, HEIGHT - 100),
        "platforms": [
            (0, HEIGHT - 40, WIDTH, 40),
            (200, 500, 100, 20),
            (400, 400, 100, 20),
            (600, 300, 100, 20),
            (750, 200, 40, 20)
        ],
        "enemies": [
            {"pos": (220, 480), "range": (200, 300)},
            {"pos": (420, 380), "range": (400, 500)},
            {"pos": (620, 280), "range": (600, 700)},
        ],
        "coins": [
            (220, 460), (420, 360), (620, 260), (760, 160)
        ]
    }
]

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = int(PLAYER_WIDTH * 1.6)  # زيادة عرض الصورة بنسبة 60%
        self.height = PLAYER_HEIGHT
        self.x_vel = 0
        self.y_vel = 0
        self.on_ground = False
        self.lives = MAX_LIVES
        self.score = 0
        try:
            self.image = pygame.image.load("MAN.png")  # تحميل صورة الشخصية
            self.image = pygame.transform.scale(self.image, (self.width, self.height))  # تغيير الحجم ليتناسب مع الأبعاد
        except pygame.error as e:
            print(f"Error loading image: {e}")
            sys.exit()

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))  # رسم الصورة على الشاشة

    def move(self, keys):
        self.x_vel = 0
        if keys[pygame.K_LEFT]:
            self.x_vel = -PLAYER_SPEED
        elif keys[pygame.K_RIGHT]:
            self.x_vel = PLAYER_SPEED
        
        # Gravity
        self.y_vel += GRAVITY
        if self.y_vel > 20:
            self.y_vel = 20

    def jump(self):
        if self.on_ground:
            self.y_vel = -PLAYER_JUMP_POWER
            self.on_ground = False

    def collision_check(self, platforms):
        # Horizontal movement
        self.x += self.x_vel
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        for p in platforms:
            plat_rect = pygame.Rect(p)
            if player_rect.colliderect(plat_rect):
                if self.x_vel > 0:
                    self.x = plat_rect.left - self.width
                elif self.x_vel < 0:
                    self.x = plat_rect.right

        # Vertical movement
        self.y += self.y_vel
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.on_ground = False
        for p in platforms:
            plat_rect = pygame.Rect(p)
            if player_rect.colliderect(plat_rect):
                if self.y_vel > 0:
                    self.y = plat_rect.top - self.height
                    self.on_ground = True
                    self.y_vel = 0
                elif self.y_vel < 0:
                    self.y = plat_rect.bottom
                    self.y_vel = 0

class Enemy:
    def __init__(self, x, y, left_limit, right_limit):
        self.x = x
        self.y = y
        self.width = ENEMY_WIDTH
        self.height = ENEMY_HEIGHT
        self.left_limit = left_limit
        self.right_limit = right_limit
        self.direction = 1

    def update(self):
        self.x += ENEMY_SPEED * self.direction
        if self.x < self.left_limit:
            self.x = self.left_limit
            self.direction = 1
        elif self.x > self.right_limit - self.width:
            self.x = self.right_limit - self.width
            self.direction = -1

    def draw(self, win):
        pygame.draw.rect(win, RED, (self.x, self.y, self.width, self.height))

class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = COIN_SIZE

    def draw(self, win):
        pygame.draw.circle(win, YELLOW, (self.x + self.size//2, self.y + self.size//2), self.size//2)

def draw_window(player, enemies, coins, platforms, level_index):
    WIN.fill(BLUE)

    # Draw platforms
    for p in platforms:
        pygame.draw.rect(WIN, BROWN, p)

    # Draw coins
    for c in coins:
        c.draw(WIN)

    # Draw enemies
    for e in enemies:
        e.draw(WIN)

    # Draw player
    player.draw(WIN)

    # Draw HUD
    text_score = FONT.render(f"Score: {player.score}", True, WHITE)
    text_lives = FONT.render(f"Lives: {player.lives}", True, WHITE)
    text_level = FONT.render(f"Level: {level_index+1}", True, WHITE)
    WIN.blit(text_score, (10, 10))
    WIN.blit(text_lives, (10, 40))
    WIN.blit(text_level, (10, 70))
    
    pygame.display.update()

def level_complete_screen(level_number, score):
    while True:
        WIN.fill(BLACK)
        complete_text = BIG_FONT.render(f"Level {level_number} completed!", True, WHITE)
        score_text = FONT.render(f"Score: {score}", True, WHITE)
        info = FONT.render("Press ENTER to continue", True, WHITE)

        WIN.blit(complete_text, (WIDTH//2 - complete_text.get_width()//2, HEIGHT//2 - 100))
        WIN.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
        WIN.blit(info, (WIDTH//2 - info.get_width()//2, HEIGHT//2 + 100))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

def congratulation_screen(score):
    # Congratulation screen after finishing level 5
    while True:
        WIN.fill(BLACK)
        text = BIG_FONT.render("Congratulations!", True, WHITE)
        score_text = FONT.render(f"Your Score: {score}", True, WHITE)
        info = FONT.render("You finished all levels! Press ESC to exit.", True, WHITE)

        WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 100))
        WIN.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
        WIN.blit(info, (WIDTH//2 - info.get_width()//2, HEIGHT//2 + 100))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

def end_screen(score):
    # Game Over screen if the player loses all lives
    while True:
        WIN.fill(BLACK)
        text = BIG_FONT.render("Game Over", True, WHITE)
        score_text = FONT.render(f"Your Score: {score}", True, WHITE)
        info = FONT.render("Press ESC to Exit", True, WHITE)

        WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 100))
        WIN.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
        WIN.blit(info, (WIDTH//2 - info.get_width()//2, HEIGHT//2 + 100))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

def main_game():
    level_index = 0
    player = Player(*levels[level_index]["start_pos"])
    platforms = levels[level_index]["platforms"]
    enemies = [Enemy(e["pos"][0], e["pos"][1], e["range"][0], e["range"][1]) for e in levels[level_index]["enemies"]]
    coins = [Coin(c[0], c[1]) for c in levels[level_index]["coins"]]

    running = True
    while running:
        clock.tick(FPS)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()

        # Player movement
        player.move(keys)
        player.collision_check(platforms)

        # Update enemies
        for e in enemies:
            e.update()

        # Check collision with enemies
        player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
        for e in enemies:
            enemy_rect = pygame.Rect(e.x, e.y, e.width, e.height)
            if player_rect.colliderect(enemy_rect):
                # Lose a life
                player.lives -= 1
                # Reset player position
                player.x, player.y = levels[level_index]["start_pos"]
                player.x_vel, player.y_vel = 0, 0
                if player.lives <= 0:
                    return ("lose", player.score)

        # Check collision with coins
        for c in coins[:]:
            coin_rect = pygame.Rect(c.x, c.y, c.size, c.size)
            if player_rect.colliderect(coin_rect):
                player.score += 10
                coins.remove(c)

        # If all coins collected in this level
        if len(coins) == 0:
            level_complete_screen(level_index+1, player.score)
            level_index += 1
            if level_index >= len(levels):
                # Finished all levels
                return ("win", player.score)
            else:
                # Load next level
                player = Player(*levels[level_index]["start_pos"])
                platforms = levels[level_index]["platforms"]
                enemies = [Enemy(e["pos"][0], e["pos"][1], e["range"][0], e["range"][1]) for e in levels[level_index]["enemies"]]
                coins = [Coin(c[0], c[1]) for c in levels[level_index]["coins"]]

        draw_window(player, enemies, coins, platforms, level_index)

def start_screen():
    # Start screen
    while True:
        WIN.fill(BLACK)
        title = BIG_FONT.render("Platformer Game", True, WHITE)
        info = FONT.render("Press ENTER to Start", True, WHITE)
        WIN.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 100))
        WIN.blit(info, (WIDTH//2 - info.get_width()//2, HEIGHT//2))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

def main():
    start_screen()
    result, final_score = main_game()
    if result == "win":
        # Congratulation screen
        congratulation_screen(final_score)
    else:
        # Game Over screen
        end_screen(final_score)

if __name__ == "__main__":
    main()
