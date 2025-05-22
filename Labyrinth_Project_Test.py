import pygame
import sys
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.init()
pygame.display.set_caption("Labyrinth Spiel")
clock = pygame.time.Clock()

screensize = (1280, 720)
screen = pygame.display.set_mode(screensize)

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, dangerous=False):
        super().__init__()
        self.image = pygame.image.load("wall.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (300, 150))  
        self.rect = self.image.get_rect(topleft=(x, y))
        self.dangerous = dangerous

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (186, 186))  
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 10
        self.hit_cooldown = 0  # Cooldown-Zähler in Frames (60 Frames = 2 Sekunden)

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

        # Horizontale Bewegung + Kollision prüfen
        self.rect.x += dx
        collided_wall = pygame.sprite.spritecollideany(self, walls)
        if collided_wall:
            self.rect.x -= dx
            if getattr(collided_wall, "dangerous", False) and self.hit_cooldown == 0:
                lives -= 1
                print("Leben verloren! Verbleibend:", lives)
                self.hit_cooldown = 60

        # Vertikale Bewegung + Kollision prüfen
        self.rect.y += dy
        collided_wall = pygame.sprite.spritecollideany(self, walls)
        if collided_wall:
            self.rect.y -= dy
            if getattr(collided_wall, "dangerous", False) and self.hit_cooldown == 0:
                lives -= 1
                print("Leben verloren! Verbleibend:", lives)
                self.hit_cooldown = 60

        # Cooldown-Timer runterzählen
        if self.hit_cooldown > 0:
            self.hit_cooldown -= 1

wallGroup = pygame.sprite.Group()
wallGroup.add(Wall(100, 200, dangerous=True))  
wallGroup.add(Wall(450, 200, dangerous=True))  
wallGroup.add(Wall(800, 200,dangerous=True)) 

player = Player(500, 500)
playerGroup = pygame.sprite.Group(player)

start_time = pygame.time.get_ticks()
max_time = 120_000  # 2 Minuten
lives = 3
font = pygame.font.SysFont(None, 48)

running = True
game_over = False

while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        keys = pygame.key.get_pressed()
        player.update(keys, wallGroup)

        # Game Over prüfen
        if lives <= 0:
            game_over = True

        # Sprites zeichnen
        wallGroup.draw(screen)
        playerGroup.draw(screen)

        # Lebensanzeige
        lives_text = font.render(f"Leben: {lives}", True, (255, 0, 0))
        screen.blit(lives_text, (20, 20))

    else:
        game_over_text = font.render("Game Over!", True, (255, 255, 255))
        screen.blit(game_over_text, (screensize[0] // 2 - 100, screensize[1] // 2 - 24))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()