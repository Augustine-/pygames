from settings import *

class Sprite(pg.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)

class AnimatedSprite(Sprite):
    def __init__(self, frames, pos, groups):
        self.frames = frames
        self.frame_index = 0
        self.animation_speed = 10
        super().__init__(pos, self.frames[self.frame_index], groups)

    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]


class Player(AnimatedSprite):
    def __init__(self, pos, groups, collision_sprites, frames):
        super().__init__(frames, pos, groups)

        # animation
        self.flip = False
        self.frames = []
        self.load_images()
        self.frame_index = 0

        # image
        self.image = self.frames[0]
        self.rect = self.image.get_frect(center = pos)

        # movement
        self.on_floor = False
        self.speed = 400
        self.gravity = 50
        self.direction = Vector2()
        self.collision_sprites = collision_sprites


    def load_images(self):
        for path, _, files in walk(join('images', 'player')):
            for file in sorted(files, key=lambda name: int(name.split('.')[0])):
                self.frames.append(pg.image.load(join(path, file)).convert_alpha())

    def input(self):
        keys = pg.key.get_pressed()
        self.direction.x = int(keys[pg.K_d]) - int(keys[pg.K_a])

        if keys[pg.K_SPACE] and self.on_floor:
            self.direction.y = -20


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
        self.check_floor()
        self.input()
        self.move(dt)
        self.animate(dt)




