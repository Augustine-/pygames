from settings import *
from math import sin
from timer import Timer
from random import randint

class Sprite(pg.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)

class Bullet(Sprite):
    def __init__(self, pos, surf, groups, direction):
        super().__init__(pos, surf, groups)

        # adjust
        self.image =  pg.transform.flip(self.image, direction == -1, False)

        # movement
        self.direction = direction
        self.speed = 850

    def update(self, dt):
        self.rect.x += self.direction * self.speed * dt

class Fire(Sprite):
    def __init__(self, pos, surf, groups, player):
        super().__init__(pos, surf, groups)
        self.player = player
        self.flip = player.flip
        self.timer = Timer(100, autostart = True, func = self.kill)
        self.y_offset = Vector2(0, 8)

        if self.player.flip:
            self.rect.midright = self.player.rect.midleft + self.y_offset
            self.image = pg.transform.flip(self.image, True, False)
        else:
            self.rect.midleft = self.player.rect.midright + self.y_offset

    def update(self, _):
        self.timer.update()

        if self.player.flip:
            self.rect.midright = self.player.rect.midleft + self.y_offset
        else:
            self.rect.midleft = self.player.rect.midright + self.y_offset

        if self.flip != self.player.flip:
            self.kill()

class AnimatedSprite(Sprite):
    def __init__(self, frames, pos, groups):
        self.frames = frames
        self.frame_index = 0
        self.animation_speed = 10
        super().__init__(pos, self.frames[self.frame_index], groups)

    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]

    def update(self, dt):
        self.animate(dt)


class Player(AnimatedSprite):
    def __init__(self, frames, pos, groups, collision_sprites, spawn_bullet):
        super().__init__(frames, pos, groups)
        self.flip = False

        # movement
        self.on_floor = False
        self.speed = 400
        self.gravity = 50
        self.direction = Vector2()
        self.collision_sprites = collision_sprites

        # timer
        self.shoot_timer = Timer(500)

        # bullet
        self.spawn_bullet = spawn_bullet


    def load_images(self):
        for path, _, files in walk(join('images', 'player')):
            for file in sorted(files, key=lambda name: int(name.split('.')[0])):
                self.frames.append(pg.image.load(join(path, file)).convert_alpha())

    def input(self):
        keys = pg.key.get_pressed()
        self.direction.x = int(keys[pg.K_d]) - int(keys[pg.K_a])

        if keys[pg.K_SPACE] and self.on_floor:
            self.direction.y = -20

        if keys[pg.K_s] and not self.shoot_timer:
            self.spawn_bullet(self.rect.center, -1 if self.flip else 1)
            self.shoot_timer.activate()


    def move(self, dt):
        # horizontal
        self.rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')

        # vertical
        self.direction.y += self.gravity * dt
        self.rect.y += self.direction.y
        self.collision('vertical')


    def collision(self, axis):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if axis == 'horizontal':
                    if self.direction.x > 0: self.rect.right = sprite.rect.left
                    if self.direction.x < 0: self.rect.left = sprite.rect.right
                else:
                    if self.direction.y > 0: self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0: self.rect.top = sprite.rect.bottom
                    self.direction.y = 0


    def animate(self, dt):
        if self.direction.x:
            self.frame_index += self.animation_speed * dt
            self.flip = self.direction.x < 0
        else:
            self.frame_index = 0

        if not self.on_floor:
            self.frame_index = 1

        self.image = self.frames[int(self.frame_index % len(self.frames))]
        self.image = pg.transform.flip(self.image, self.flip, False)


    # this would be a good way to detect wall or ceiling collisions, for a more advanced platformer
    def check_floor(self):
        # use move_to to adjust the position of a rect, the default is always topleft
        bottom_rect = pg.FRect((0, 0), (self.rect.width, 2)).move_to(midtop = self.rect.midbottom)
        level_rects = [sprite.rect for sprite in self.collision_sprites]
        self.on_floor = True if bottom_rect.collidelist(level_rects) >= 0 else False

    def update(self, dt):
        self.shoot_timer.update()
        self.check_floor()
        self.input()
        self.move(dt)
        self.animate(dt)


class Enemy(AnimatedSprite):
    def __init__(self, frames, pos, groups):
        super().__init__(frames, pos, groups)

        self.death_timer = Timer(200, func = self.kill)

    def update(self, dt):
        self.death_timer.update()
        if not self.death_timer:
            self.move(dt)
            self.animate(dt)
        self.constraint()

    def destroy(self):
        self.death_timer.activate()
        self.animation_speed = 0
        self.image = pg.mask.from_surface(self.image).to_surface()
        self.image.set_colorkey('black')

class Worm(Enemy):
    def __init__(self, frames, rect, groups):
        super().__init__(frames, rect.topleft, groups)
        self.rect.bottomleft = rect.bottomleft
        self.main_rect = rect
        self.speed = randint(160, 200)
        self.direction   = 1

    def move(self, dt):
        self.rect.x += self.speed * self.direction * dt

    def constraint(self):
       if not self.main_rect.contains(self.rect):
           self.direction *= -1
           self.frames = [pg.transform.flip(surf, True, False) for surf in self.frames]

class Bee(Enemy):
    def __init__(self, frames, pos, groups, speed):
        super().__init__(frames, pos, groups)
        self.speed = speed
        self.amplitude = randint(500, 600)
        self.frequency = randint(300, 600)

    def move(self, dt):
        self.rect.x -= self.speed * dt
        self.rect.y += sin(pg.time.get_ticks() / self.frequency) * self.amplitude * dt

    def constraint(self):
        if self.rect.right <= 0:
            self.kill()
