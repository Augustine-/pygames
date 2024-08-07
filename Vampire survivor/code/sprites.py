from settings import *
from math import atan2, degrees, pi, cos, sin
from random import randint, uniform


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
        self.ground = True

class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)

class Gun(pygame.sprite.Sprite):
    def __init__(self, player, groups) -> None:
        # player connection
        self.player = player
        self.distance = 140
        self.player_direction = Vector2(1, 0)

        # sprite
        super().__init__(groups)
        self.surf = pygame.image.load(join('images', 'gun', 'gun.png')).convert_alpha()
        self.image = self.surf
        self.rect = self.image.get_frect(center = self.player.rect.center + (self.distance * self.player_direction))

    def get_direction(self):
        mouse_pos = Vector2(pygame.mouse.get_pos())
        player_pos = Vector2(WINDOW_CENTER)
        self.player_direction = (mouse_pos - player_pos).normalize()

    def rotate_gun(self):
        angle = degrees(atan2(self.player_direction.x, self.player_direction.y)) -90
        if self.player_direction.x > 0:
            self.image = pygame.transform.rotozoom(self.surf, angle, 1)
        else:
            self.image = pygame.transform.rotozoom(self.surf, abs(angle), 1)
            self.image = pygame.transform.flip(self.image, False, True)


    def update(self, _):
        self.get_direction()
        self.rect.center = self.player.rect.center + (self.player_direction * self.distance)
        self.rotate_gun()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, surf, pos, direction, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = pos)
        self.direction = direction
        self.speed = 1000
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 2000

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt

        if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, player, collision_sprites):
        super().__init__(groups)
        self.player = player

        # image
        self.frame_index = 0
        self.frames = frames
        self.image = frames[self.frame_index]
        self.animation_speed = 5

        # rect
        self.rect = self.image.get_frect(center = pos)
        self.hitbox = self.rect.inflate(-20, -40)
        self.collision_sprites = collision_sprites
        self.direction = Vector2()
        self.speed = 100


    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.hitbox.right = sprite.rect.left
                    if self.direction.x < 0: self.hitbox.left = sprite.rect.right
                else:
                    if self.direction.y > 0: self.hitbox.bottom = sprite.rect.top
                    if self.direction.y < 0: self.hitbox.top = sprite.rect.bottom

    def get_direction(self):
        player_pos = Vector2(self.player.hitbox.center)
        enemy_pos = Vector2(self.rect.center)
        self.direction = (player_pos - enemy_pos).normalize()

    def move(self, dt):
        self.hitbox.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * self.speed * dt
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]

    def update(self, dt):
        self.get_direction()
        self.move(dt)
        self.animate(dt)
