from settings import *
from random import randint, uniform


class Game:
    def __init__(self):
        pg.init()

        # display
        pg.display.set_caption('ping')
        self.screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        # pg.mouse.set_visible(False)

        # time
        self.clock = pg.time.Clock()
        self.running = True

        # groups
        self.all_sprites = pg.sprite.Group()

        self.setup()

    def setup(self):
        self.player = Paddle('player', self.all_sprites)
        self.opponent = Paddle('opponent', self.all_sprites)
        self.ball = Ball(self.all_sprites)

    def input(self, dt):
        keys = pg.key.get_pressed()
        self.player.direction.y = max(int(keys[pg.K_s]), int(keys[pg.K_d])) - max(int(keys[pg.K_w]), int(keys[pg.K_a]))
        self.player.rect.center += self.player.direction * self.player.speed * dt

        if self.player.rect.top <= 0:
            self.player.rect.top = 0
        if self.player.rect.bottom >= WINDOW_HEIGHT - 1:
            self.player.rect.bottom = WINDOW_HEIGHT - 1


    def run(self):
        while self.running:
            dt = self.clock.tick(144) / 1000

            # events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

            # updates
            self.input(dt)
            self.all_sprites.update(dt)

            # render
            self.screen.fill(COLORS['bg'])
            self.all_sprites.draw(self.screen)

            pg.display.update()
        pg.quit()


class Paddle(pg.sprite.Sprite):
    def __init__(self, side, groups):
        super().__init__(groups)
        self.image = pg.Surface(SIZE['paddle'])
        self.rect = pg.FRect(POS[side], SIZE['paddle'])
        self.pos = POS[side]
        self.speed = SPEED[side]
        self.direction = Vector2()

        self.image.fill(COLORS['paddle'])

class Ball(pg.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pg.Surface(SIZE['ball'], pg.SRCALPHA)
        pg.draw.circle(self.image, COLORS['ball'], (15, 15), radius = 15)
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

        self.direction = Vector2(uniform(-1, 1), uniform(-1, 1))
        self.speed = SPEED['ball']

    def move(self, dt):
        if self.rect.left <= 0 or self.rect.right >= WINDOW_WIDTH:
            self.direction.x *= -1
        if self.rect.top <= 0 or self.rect.bottom >= WINDOW_HEIGHT:
            self.direction.y *= -1

        self.rect.center += self.direction * self.speed * dt

    def update(self, dt):
        self.move(dt)





if __name__ == '__main__':
    g = Game()
    g.run()
