from settings import *
from random import uniform, choice

class Paddle(pg.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

        # image
        self.image = pg.Surface(SIZE['paddle'], pg.SRCALPHA)
        pg.draw.rect(self.image, COLORS['paddle'], pg.FRect((0, 0), SIZE['paddle']), 0, 5)
        self.rect = self.image.get_frect(center = POS['player'])
        self.old_rect = self.rect.copy()

        # rect & movement
        self.direction = 0

    def move(self, dt):
        self.rect.centery += self.direction * self.speed * dt

        self.rect.top = 0 if self.rect.top < 0 else self.rect.top
        self.rect.bottom = WINDOW_HEIGHT if self.rect.bottom > WINDOW_HEIGHT else self.rect.bottom

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.get_direction()
        self.move(dt)

class Opponnent(Paddle):
    def __init__(self, groups, ball):
        super().__init__(groups)
        self.rect.center = POS['opponent']
        self.speed = SPEED['opponent']
        self.direction = 0
        self.old_rect = self.rect.copy()

        self.ball = ball

    def get_direction(self):
        if self.rect.centery < self.ball.rect.centery:
            self.direction = 1
        elif self.rect.centery > self.ball.rect.centery:
            self.direction = -1
        else:
            self.direction = 0

class Player(Paddle):
    def __init__(self, groups):
        super().__init__(groups)
        self.rect = self.image.get_frect(center = POS['player'])
        self.speed = SPEED['player']

    def get_direction(self):
        keys = pg.key.get_pressed()
        self.direction = max(int(keys[pg.K_s]), int(keys[pg.K_d])) - max(int(keys[pg.K_w]), int(keys[pg.K_a]))


class Ball(pg.sprite.Sprite):
    def __init__(self, groups, paddle_sprites, update_score):
        super().__init__(groups)
        self.update_score = update_score

        # image
        self.image = pg.Surface(SIZE['ball'], pg.SRCALPHA)
        pg.draw.circle(self.image, COLORS['ball'], (SIZE['ball'][0] / 2, SIZE['ball'][1] / 2), radius = SIZE['ball'][1] / 2)
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.old_rect = self.rect.copy()

        # rect and movement
        self.direction = Vector2(choice((-1, 1)), uniform(0.4, 0.8) * choice((-1, 1)))
        self.speed = SPEED['ball']

        # sprites
        self.paddle_sprites = paddle_sprites


    def move(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        self.rect.y += self.direction.y * self.speed * dt
        self.collision('vertical')

    def collision(self, direction):
        for sprite in self.paddle_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == 'horizontal':
                    if self.rect.right >= sprite.rect.left and self.old_rect.right < sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                        self.direction.x *= -1
                    elif self.rect.left <= sprite.rect.right and self.old_rect.left > sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                        self.direction.x *= -1
                else:
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                        self.direction.y *= -1
                    elif self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                        self.direction.y *= -1


    def wall_collision(self):
        r = self.rect
        if r.top <= 0:
            r.top = 0
            self.direction.y *= -1

        if r.bottom >= WINDOW_HEIGHT:
            r.bottom = WINDOW_HEIGHT
            self.direction.y *= -1

        # testing only
        if r.left <= 0:
            self.update_score('player')
            self.reset()
        elif r.right >= WINDOW_WIDTH:
            self.update_score('opponent')
            self.reset()

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.move(dt)
        self.wall_collision()

    def reset(self):
        self.rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        self.direction = Vector2(choice((-1, 1)), uniform(0.4, 0.8) * choice((-1, 1)))