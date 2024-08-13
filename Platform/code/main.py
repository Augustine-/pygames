from settings import *
from sprites import *
from player import Player
from groups import AllSprites


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pg.display.set_caption('Platformer')
        self.clock = pg.time.Clock()
        self.running = True

        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = AllSprites()

        # setup
        self.setup()
        self.player = Player(self.all_sprites, self.collision_sprites)

    def load_images(self):
        pass

    def setup(self):
        map = load_pygame(join('data', 'maps', 'world.tmx'))
        # self.music.play(loops = -1)

        for x, y, image in map.get_layer_by_name('Main').tiles():
            Sprite((x*TILE_SIZE, y*TILE_SIZE), image, (self.all_sprites, self.collision_sprites))

    def run(self):
        while self.running:
            dt = self.clock.tick(FRAMERATE) / 1000

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

            # update
            self.all_sprites.update(dt)

            # draw
            self.screen.fill(BG_COLOR)
            self.all_sprites.draw(self.player.rect.center)
            pg.display.update()

        pg.quit()

if __name__ == '__main__':
    game = Game()
    game.run()