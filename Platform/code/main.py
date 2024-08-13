from settings import *
from sprites import *
from util import *
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
        self.load_assets()
        self.setup()


    def load_assets(self):
        # graphics
        self.player_frames = import_folder('images', 'player')
        self.bee_frames = import_folder('images', 'enemies', 'bee')
        self.worm_frames = import_folder('images', 'enemies', 'worm')
        self.bullet_surf = import_image('images', 'gun', 'bullet')
        self.fire_surf = import_image('images', 'gun', 'fire')

        # audio

    def setup(self):
        map = load_pygame(join('data', 'maps', 'world.tmx'))
        # self.music.play(loops = -1)

        for x, y, image in map.get_layer_by_name('Main').tiles():
            Sprite((x*TILE_SIZE, y*TILE_SIZE), image, (self.all_sprites, self.collision_sprites))

        for x, y, image in map.get_layer_by_name('Decoration').tiles():
            Sprite((x*TILE_SIZE, y*TILE_SIZE), image, (self.all_sprites))

        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites, self.player_frames)

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