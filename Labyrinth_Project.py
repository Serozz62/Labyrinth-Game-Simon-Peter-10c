import pygame
import sys
import os
 
os.chdir(os.path.dirname(os.path.abspath(__file__)))
 
pygame.init()
pygame.display.set_caption("Labyrinth Spiel")
clock = pygame.time.Clock()
 
screensize = (800, 600)
screen = pygame.display.set_mode(screensize)
 
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("wall.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (150, 75))
        self.rect = self.image.get_rect(topleft=(x, y))
 
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (83, 93))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 10
 
    def update(self, key, walls):
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
 
wallGroup = pygame.sprite.Group()
wallGroup.add(Wall(50, 100))
wallGroup.add(Wall(200, 100))
wallGroup.add(Wall(350, 100))
 
player = Player(300, 300)
playerGroup = pygame.sprite.Group(player)
 
start_time = pygame.time.get_ticks()
max_time = 120_000  # 120 Sekunden
lives = 3
 
running = True
while running:
    screen.fill((0, 0, 0))  # Bildschirm löschen
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
 
    keys = pygame.key.get_pressed()
    player.update(keys, wallGroup)
 
    wallGroup.draw(screen)
    playerGroup.draw(screen)
 
    pygame.display.flip()
    clock.tick(30)
 
pygame.quit()
sys.exit()