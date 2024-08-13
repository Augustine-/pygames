from settings import *
from sprites import *
from util import *
from groups import AllSprites
from random import randint


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
        self.enemy_sprites = AllSprites()
        self.bullet_sprites = AllSprites()

        # setup
        self.load_assets()
        self.setup()

        # timers
        self.bee_timer = Timer(500, func = self.spawn_bee, autostart = True, repeat = True)

    def spawn_bee(self):
        Bee(
            frames = self.bee_frames,
            pos = (self.level_width + WINDOW_WIDTH, randint(0, self.level_height)),
            groups = (self.all_sprites, self.enemy_sprites),
            speed = randint(300, 500)
        )

    def spawn_bullet(self, pos, direction):
        x = pos[0] + direction * 34 if direction == 1 else pos[0] + direction * 34 - self.bullet_surf.get_width()
        Bullet((x, pos[1]), self.bullet_surf, (self.all_sprites, self.bullet_sprites), direction)
        Fire(pos, self.fire_surf, self.all_sprites, self.player)
        self.audio['shoot'].play()


    def load_assets(self):
        # graphics
        self.player_frames = import_folder('images', 'player')
        self.bee_frames = import_folder('images', 'enemies', 'bee')
        self.worm_frames = import_folder('images', 'enemies', 'worm')
        self.bullet_surf = import_image('images', 'gun', 'bullet')
        self.fire_surf = import_image('images', 'gun', 'fire')

        # audio
        self.audio = import_audio('audio')

    def setup(self):
        map = load_pygame(join('data', 'maps', 'world.tmx'))
        self.level_width = map.width * TILE_SIZE
        self.level_height = map.height * TILE_SIZE

        for x, y, image in map.get_layer_by_name('Main').tiles():
            Sprite((x*TILE_SIZE, y*TILE_SIZE), image, (self.all_sprites, self.collision_sprites))

        for x, y, image in map.get_layer_by_name('Decoration').tiles():
            Sprite((x*TILE_SIZE, y*TILE_SIZE), image, (self.all_sprites))

        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player(self.player_frames, (obj.x, obj.y), self.all_sprites, self.collision_sprites, self.spawn_bullet)
            elif obj.name == 'Worm':
                Worm(self.worm_frames, pg.FRect(obj.x, obj.y, obj.width, obj.height), (self.all_sprites, self.enemy_sprites))

        self.audio['music'].play(loops = -1)


    def run(self):
        while self.running:
            dt = self.clock.tick(FRAMERATE) / 1000

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

            # update
            self.bee_timer.update()
            self.all_sprites.update(dt)
            self.collision()

            # draw
            self.screen.fill(BG_COLOR)
            self.all_sprites.draw(self.player.rect.center)
            pg.display.update()

        pg.quit()

    def collision(self):
        for bullet in self.bullet_sprites:
            sprite_collision = pg.sprite.spritecollide(bullet, self.enemy_sprites, False, pg.sprite.collide_mask)
            if sprite_collision:
                self.audio['impact'].play()
                bullet.kill()
                for sprite in sprite_collision:
                    sprite.destroy()

        if pg.sprite.spritecollide(self.player, self.enemy_sprites, False, pg.sprite.collide_mask):
            self.running = False

if __name__ == '__main__':
    game = Game()
    game.run()