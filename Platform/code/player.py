from settings import *

class Player(pg.sprite.Sprite):
    def __init__(self, groups, collision_sprites):
        super().__init__(groups)
        # animation
        self.frames = []
        self.load_images()
        self.frame_index = 0

        # image
        self.image = self.frames[0]
        self.rect = self.image.get_frect(center = WINDOW_CENTER)

        # movement
        self.speed = 400
        self.direction = Vector2()
        self.collision_sprites = collision_sprites

    def load_images(self):
        for path, _, files in walk(join('images', 'player')):
            for file in sorted(files, key=lambda name: int(name.split('.')[0])):
                self.frames.append(pg.image.load(join(path, file)).convert_alpha())

    def input(self):
        keys = pg.key.get_pressed()
        self.direction.x = int(keys[pg.K_d]) - int(keys[pg.K_a])
        self.direction.y = int(keys[pg.K_s]) - int(keys[pg.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction

    def move(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        self.rect.y += self.direction.y * self.speed * dt
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

    def animate(self, dt):
        self.frame_index += self.frame_index + 1 * dt if self.direction else 0
        self.image = self.frames[int(self.frame_index % len(self.frames))]

    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)


