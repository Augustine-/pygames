import pygame
from random import randint, uniform
from os.path import join

# general setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
WINDOW_CENTER = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
pygame.display.set_caption("space")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
running = True
clock = pygame.time.Clock()

# imports
star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha()
meteor_surf = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
laser_surf = pygame.image.load(join('images', 'laser.png')).convert_alpha()
explosion_frames = [pygame.image.load(join('images', 'explosion', f'{i}.png')).convert_alpha() for i in range(21)]
font = pygame.font.Font(join('images', 'Oxanium-bold.ttf'), 50)

laser_sound = pygame.mixer.Sound(join('audio', 'laser.wav'))
laser_sound.set_volume(0.2)

explosion_sound = pygame.mixer.Sound(join('audio', 'explosion.wav'))
explosion_sound.set_volume(0.2)

game_music = pygame.mixer.Sound(join('audio', 'game_music.wav'))
game_music.set_volume(0.2)
game_music.play(loops = -1)

# classes
class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = frames[self.frame_index]
        self.rect = self.image.get_frect(center = pos)

    def update(self, dt):
        self.frame_index += 20 * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index) % len(self.frames)]
        else:
            self.kill()

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        #init parent class
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center = WINDOW_CENTER)
        self.direction = pygame.Vector2()
        self.speed = 300
        self.mask = pygame.mask.from_surface(self.image)

        # cooldown (ms)
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400


    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def update(self, dt):
        recent_keys = pygame.key.get_just_pressed()
        keys = pygame.key.get_pressed()

        # movement
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        # weapon
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surf, self.rect.midtop, (all_sprites, laser_sprites))
            laser_sound.play()
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()

        self.laser_timer()

class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)

    def update(self, dt):
        self.rect.centery -= 600 * dt

        if self.rect.bottom < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.original_surf = surf
        self.image = surf
        self.rect = self.image.get_frect(center = pos)
        self.birthday = pygame.time.get_ticks()
        self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(400, 500)
        self.rotation = 0
        self.rotation_speed = randint(-80, 80)

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_surf, self.rotation, 1)
        self.rect = self.image.get_frect(center = self.rect.center)

        current_time = pygame.time.get_ticks()
        if current_time - self.birthday >= 3000:
            self.kill()

def collisions():
    global running
    if pygame.sprite.spritecollide(player, meteor_sprites, True, pygame.sprite.collide_mask):
        print('player/meteor coll')
        running = False

    for laser in laser_sprites:
        laser_hits = pygame.sprite.spritecollide(laser, meteor_sprites, True)
        if laser_hits:
            laser.kill()
            AnimatedExplosion(explosion_frames, laser.rect.midtop , all_sprites)
            explosion_sound.play()

def display_score():
    current_time = pygame.time.get_ticks()
    text_surf = font.render(str(current_time), True, (200, 50, 100))
    text_rect = text_surf.get_frect(midbottom = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50))
    screen.blit(text_surf, text_rect)
    pygame.draw.rect(screen, 'white', text_rect.inflate(30, 20).move(0,-8), 5, 10)

# groups
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()

# sprites
stars = [Star(all_sprites, star_surf) for i in range(20)]
laser_rect = laser_surf.get_frect(left = 20, bottom = WINDOW_HEIGHT - 20)
player = Player(all_sprites)

# custom events
## meteor
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)

while running:
    dt = clock.tick(144) / 1000
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            x, y = randint(0, WINDOW_WIDTH), randint(-200, -100)
            Meteor(meteor_surf, (x, y), (all_sprites, meteor_sprites))

    # update
    all_sprites.update(dt)
    collisions()

    # render
    screen.fill('darkblue')
    all_sprites.draw(screen)
    display_score()

    pygame.display.update()
pygame.quit()