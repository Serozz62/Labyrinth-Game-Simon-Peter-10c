import pygame
import sys
import os
 
os.chdir(os.path.dirname(os.path.abspath(__file__)))
 
pygame.init()
pygame.display.set_caption("Labyrinth Spiel")
clock = pygame.time.Clock()
 
TILE_SIZE = 60
GRID_WIDTH = 20
GRID_HEIGHT = 12
screensize = (TILE_SIZE * GRID_WIDTH, TILE_SIZE * GRID_HEIGHT)
screen = pygame.display.set_mode(screensize)
 
GRAY = (100, 100, 100)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
 
 
font = pygame.font.SysFont(None, 48)
big_font = pygame.font.SysFont(None, 72)
button_rect = pygame.Rect(screensize[0] // 2 - 100, screensize[1] // 2 + 40, 200, 50)
 
pygame.mixer.init()
 
game_over = False
game_won = False
 
mazes = [
    [  # Level 1
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,1,0,1],
        [1,0,1,1,1,0,0,0,1,0,0,0,1,0,1,1,0,1,0,1],
        [1,0,1,0,1,1,1,0,1,1,1,0,1,0,1,1,0,1,0,1],
        [1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,1,0,1],
        [1,0,1,1,1,0,1,1,1,0,1,1,1,1,1,1,0,1,0,1],
        [1,0,1,1,1,0,0,0,1,0,1,0,0,0,0,1,0,1,0,1],
        [1,0,1,0,1,1,1,0,1,1,1,0,1,1,0,1,0,1,0,1],
        [1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,0,0,0,1],
        [1,1,0,1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,0,1],
        [1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,1,9,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    ],
    [  # Level 2
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,0,1,0,1,1,0,1,0,1,1,1,1,0,1],
        [1,0,0,0,0,1,0,0,0,1,0,0,1,0,0,0,0,1,0,1],
        [1,0,1,1,0,1,1,1,0,1,0,1,1,1,1,1,0,1,0,1],
        [1,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1],
        [1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,9,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1],
    ]
]
 
current_level_index = 0  
goal_rect = pygame.Rect((0, 0, TILE_SIZE, TILE_SIZE))
 
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("wall.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=(x, y))
 
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5
 
    def update(self, keys, walls):
        global lives
 
        dx, dy = 0, 0
        if keys[pygame.K_a]: dx = -self.speed
        if keys[pygame.K_d]: dx = self.speed
        if keys[pygame.K_w]: dy = -self.speed
        if keys[pygame.K_s]: dy = self.speed
 
        self.rect.x += dx
        if pygame.sprite.spritecollideany(self, walls):
            self.rect.x -= dx
 
        self.rect.y += dy
        if pygame.sprite.spritecollideany(self, walls):
            self.rect.y -= dy
 
        self.rect.clamp_ip(screen.get_rect())
 
def create_level():
    global goal_rect
    walls = pygame.sprite.Group()
    level = mazes[current_level_index]
    for y, row in enumerate(level):
        for x, tile in enumerate(row):
            px, py = x * TILE_SIZE, y * TILE_SIZE
            if tile == 1:
                walls.add(Wall(px, py))
            elif tile == 9:
                goal_rect = pygame.Rect(px, py, TILE_SIZE, TILE_SIZE)
    return walls
 
def reset_game(next_level=False):
    global lives, game_over, game_won, wallGroup, player, current_level_index
 
    if next_level:
        current_level_index += 1
        if current_level_index >= len(mazes):
            current_level_index = 0  
 
    lives = 3
    game_over = False
    game_won = False
    wallGroup = create_level()
    player_start_y = TILE_SIZE * (len(mazes[current_level_index]) - 2)
    player = Player(TILE_SIZE, player_start_y)
 
    return player
 
player = reset_game()
playerGroup = pygame.sprite.Group(player)
 
running = True
while running:
    screen.fill((0, 0, 0))
    keys = pygame.key.get_pressed()
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and (game_over or game_won):
            if button_rect.collidepoint(event.pos):
                player = reset_game(next_level=game_won)
                playerGroup = pygame.sprite.Group(player)
 
    if not game_over and not game_won:
        player.update(keys, wallGroup)
 
        if player.rect.colliderect(goal_rect):
            game_won = True
 
        if lives <= 0:
            game_over = True
 
        wallGroup.draw(screen)
        playerGroup.draw(screen)
 
        pygame.draw.rect(screen, (0, 255, 0), goal_rect)
 
    else:
        msg = "Gewonnen!" if game_won else "Game Over!"
        end_text = big_font.render(msg, True, WHITE)
        screen.blit(end_text, (screensize[0] // 2 - 120, screensize[1] // 2 - 50))
        pygame.draw.rect(screen, (150, 150, 150), button_rect)
        button_text = font.render("Nächstes Level" if game_won else "Replay", True, (0, 0, 0))
        screen.blit(button_text, (button_rect.x + 20, button_rect.y + 10))
 
    pygame.display.flip()
    clock.tick(30)
 
pygame.quit()
sys.exit()
 
 