import pygame
import sys
import os
 
os.chdir(os.path.dirname(os.path.abspath(__file__)))
 
pygame.init()
pygame.display.set_caption("Labyrinth Spiel")
clock = pygame.time.Clock()
 
TILE_SIZE = 64
GRID_WIDTH = 10
GRID_HEIGHT = 10
screensize = (GRID_WIDTH * TILE_SIZE, GRID_HEIGHT * TILE_SIZE)
screen = pygame.display.set_mode(screensize)
 
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, dangerous=False):
        super().__init__()
        self.image = pygame.image.load("wall.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.dangerous = dangerous
 
class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(topleft=(x, y))
 
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = TILE_SIZE
        self.hit_cooldown = 0
 
    def update(self, key, walls):
        global lives
        dx, dy = 0, 0
        if key[pygame.K_a]:
            dx = -self.speed
        if key[pygame.K_d]:
            dx = self.speed
        if key[pygame.K_w]:
            dy = -self.speed
        if key[pygame.K_s]:
            dy = self.speed
 
        self.rect.x += dx
        if pygame.sprite.spritecollideany(self, walls):
            self.rect.x -= dx
 
        self.rect.y += dy
        if pygame.sprite.spritecollideany(self, walls):
            self.rect.y -= dy
 
        self.rect.clamp_ip(screen.get_rect())

maze = [
    [1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,1,0,1,0,0,1],
    [1,0,1,0,1,0,1,0,1,1],
    [1,0,1,0,0,0,1,0,1,1],
    [1,0,1,1,1,0,1,0,0,1],
    [1,0,0,0,1,0,1,1,0,1],
    [1,1,1,0,1,0,0,1,0,1],
    [1,0,0,0,1,1,0,1,0,1],
    [1,0,1,1,1,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1],
]
 
wallGroup = pygame.sprite.Group()
for y, row in enumerate(maze):
    for x, tile in enumerate(row):
        if tile == 1:
            wallGroup.add(Wall(x * TILE_SIZE, y * TILE_SIZE))
 
goal = Goal(1 * TILE_SIZE, 1 * TILE_SIZE)
goalGroup = pygame.sprite.Group(goal)
 
player = Player(5 * TILE_SIZE, 8 * TILE_SIZE)
playerGroup = pygame.sprite.Group(player)
 
lives = 3
font = pygame.font.SysFont(None, 48)
running = True
game_over = False
won = False
 
while running:
    screen.fill((0, 0, 0))
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
 
    if not game_over and not won:
        keys = pygame.key.get_pressed()
        player.update(keys, wallGroup)
 
        if pygame.sprite.spritecollideany(player, goalGroup):
            won = True
 
        wallGroup.draw(screen)
        goalGroup.draw(screen)
        playerGroup.draw(screen)
 
        lives_text = font.render(f"Leben: {lives}", True, (255, 0, 0))
        screen.blit(lives_text, (10, 10))
 
    elif game_over:
        game_over_text = font.render("Game Over!", True, (255, 255, 255))
        screen.blit(game_over_text, (screensize[0] // 2 - 100, screensize[1] // 2 - 24))
 
    elif won:
        win_text = font.render("Gewonnen!", True, (0, 255, 0))
        screen.blit(win_text, (screensize[0] // 2 - 100, screensize[1] // 2 - 24))
 
    pygame.display.flip()
    clock.tick(10)
 
pygame.quit()
sys.exit()