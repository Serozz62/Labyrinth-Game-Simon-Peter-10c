import pygame, sys, os, random
from math import hypot
 
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rogue‑Like")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont(None, 24)
BIGFONT = pygame.font.SysFont(None, 48)

ASSET_DIR = os.path.join(os.path.dirname(__file__), "assets")
def load_img(name, colorkey=None, scale=None):
    path = os.path.join(ASSET_DIR, name)
    img = pygame.image.load(path).convert_alpha()
    if scale: img = pygame.transform.scale(img, scale)
    if colorkey is not None: img.set_colorkey(colorkey)
    return img
 
PLAYER_SPEED = 200  
PLAYER_HP = 100
PLAYER_DAMAGE = 10
ENEMY_SPEED = 100
ENEMY_HP = 30
XP_PER_KILL = 50
 
XP_LEVELS = [0, 100, 250, 500, 1000, 2000, 4000]
 
class Entity(pygame.sprite.Sprite):
    def __init__(self, img, pos, speed, hp, damage):
        super().__init__()
        self.orig_img = img
        self.image = img
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(pos)
        self.vel = pygame.math.Vector2(0,0)
        self.speed = speed
        self.max_hp = hp
        self.hp = hp
        self.damage = damage
 
    def update(self, dt):
        self.pos += self.vel * dt
        self.rect.center = self.pos
 
    def is_alive(self):
        return self.hp > 0
 
class Player(Entity):
    def __init__(self, pos):
        img = load_img("player.png", scale=(40,40))
        super().__init__(img, pos, PLAYER_SPEED, PLAYER_HP, PLAYER_DAMAGE)
        self.xp = 0
        self.level = 1
        self.next_level_xp = XP_LEVELS[self.level]
        self.levelup_ready = False
        self.projectiles = pygame.sprite.Group()
 
    def handle_input(self, keys, dt):
        dirx, diry = 0,0
        if keys[pygame.K_w]: diry = -1
        if keys[pygame.K_s]: diry = 1
        if keys[pygame.K_a]: dirx = -1
        if keys[pygame.K_d]: dirx = 1
        self.vel = pygame.math.Vector2(dirx, diry).normalize() * self.speed if dirx or diry else pygame.math.Vector2(0,0)
        if keys[pygame.K_SPACE]:
            self.shoot()
 
    def shoot(self):
        now = pygame.time.get_ticks()

        if hasattr(self, 'last_shot') and now - self.last_shot < 300:
            return
        self.last_shot = now
        proj = Projectile(load_img("projectile.png", scale=(10,10)), self.rect.center, self.damage)
        mouse = pygame.mouse.get_pos()
        proj.vel = (pygame.math.Vector2(mouse) - pygame.math.Vector2(self.rect.center)).normalize() * 400
        self.projectiles.add(proj)
        all_sprites.add(proj)
 
    def gain_xp(self, amount):
        self.xp += amount
        if self.level < len(XP_LEVELS)-1 and self.xp >= XP_LEVELS[self.level]:
            self.levelup_ready = True
 
    def level_up(self):
        if not self.levelup_ready: return
        self.level += 1
        self.levelup_ready = False

        choose_skill()
        self.next_level_xp = XP_LEVELS[self.level]
 
    def draw_ui(self, surf):
        pygame.draw.rect(surf, (50,50,50), (10,10,200,25))
        pygame.draw.rect(surf, (0,200,0), (10,10, int(200*self.xp/self.next_level_xp),25))
        t = FONT.render(f"HP: {self.hp}/{self.max_hp}  LVL:{self.level}  XP:{self.xp}/{self.next_level_xp}",True,(255,255,255))
        surf.blit(t,(10,40))
 
class Projectile(pygame.sprite.Sprite):
    def __init__(self, img, pos, damage):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(pos)
        self.vel = pygame.math.Vector2(0, 0)
        self.damage = damage
 
    def update(self, dt):
        self.pos += self.vel * dt
        self.rect.center = self.pos
        if not screen.get_rect().collidepoint(self.rect.center):
            self.kill()
 
class Enemy(Entity):
    def __init__(self, pos):
        img = load_img(random.choice(["enemy1.png","enemy2.png"]), scale=(30,30))
        super().__init__(img, pos, ENEMY_SPEED, ENEMY_HP, 5)
 
    def update(self, dt):
        if player.is_alive():
            dir_vec = pygame.math.Vector2(player.pos - self.pos)
            if dir_vec.length() != 0:
                self.vel = dir_vec.normalize() * self.speed
        super().update(dt)
 
def choose_skill():
    choosing = True
    options = [
        ("+20% Schaden", lambda p: setattr(p, 'damage', p.damage*1.2)),
        ("+20% Max HP", lambda p: setattr(p, 'max_hp', int(p.max_hp*1.2)) or setattr(p, 'hp', int(p.hp*1.2))),
        ("+20% Speed", lambda p: setattr(p, 'speed', p.speed*1.2))
    ]
    while choosing:
        screen.fill((30,30,30))
        t = BIGFONT.render("Level Up! Wähle:", True, (255,255,255))
        screen.blit(t,(WIDTH//2-150,100))
        for i, (text, _) in enumerate(options):
            rect = pygame.Rect(200,200+i*80,400,60)
            pygame.draw.rect(screen,(100,100,100),rect)
            screen.blit(FONT.render(text,True,(255,255,255)),(rect.x+10,rect.y+20))
        pygame.display.flip()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                mx,my = ev.pos
                for i, opt in enumerate(options):
                    rect = pygame.Rect(200,200+i*80,400,60)
                    if rect.collidepoint((mx,my)):
                        options[i][1](player)
                        choosing = False
 
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
 
player = Player((WIDTH//2, HEIGHT//2))
all_sprites.add(player)
 
SPAWN_EVENT = pygame.USEREVENT+1
pygame.time.set_timer(SPAWN_EVENT, 2000)  # alle 2 Sekunden
 
def game_loop():
    while True:
        dt = clock.tick(60) / 1000.0
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == SPAWN_EVENT:
                ex = random.randrange(0, WIDTH)
                ey = random.choice([0, HEIGHT])
                e = Enemy((ex,ey))
                enemies.add(e); all_sprites.add(e)
 
        keys = pygame.key.get_pressed()
        player.handle_input(keys, dt)

        all_sprites.update(dt)

        for proj in player.projectiles:
            hits = pygame.sprite.spritecollide(proj, enemies, False)
            for e in hits:
                e.hp -= proj.damage
                proj.kill()
                if not e.is_alive():
                    e.kill()
                    player.gain_xp(XP_PER_KILL)

        for e in enemies:
            if pygame.sprite.collide_rect(e, player):
                player.hp -= e.damage
                e.kill()
                if player.hp <= 0:
                    game_over()
                    return

        if player.levelup_ready:
            player.level_up()
 
        screen.fill((20,20,20))
        all_sprites.draw(screen)
        player.draw_ui(screen)
        pygame.display.flip()
 
def game_over():
    t = BIGFONT.render("Game Over!", True, (255,100,100))
    screen.blit(t,(WIDTH//2-150,HEIGHT//2-30))
    pygame.display.flip()
    pygame.time.delay(2000)
    pygame.quit()
    sys.exit()
 
if __name__=="__main__":
    game_loop()
 