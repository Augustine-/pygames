from settings import *
from player import Player
from sprites import *
from random import randint
from pytmx.util_pygame import load_pygame
from groups import AllSprites
from collections import defaultdict

class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption('vampire hunters')
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.mouse.set_visible(False)
        self.running = True
        self.clock = pygame.time.Clock()

        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = AllSprites()
        self.bullet_sprites = AllSprites()
        self.enemy_sprites = AllSprites()

        # gun cooldown
        self.can_shoot = True
        self.shot_time = 0
        self.gun_cooldown = 100

        # enemies
        self.enemies = []
        self.enemy_frames = defaultdict(list)
        self.enemy_spawn_time = 0
        self.enemy_spawn_cooldown = 500


        self.setup()
        self.load_images()

    def load_images(self):
        self.bullet_surf = pygame.image.load(join('images', 'gun', 'bullet.png')).convert_alpha()

        for enemy in self.enemies:
            for path, _, files in walk(join('images', 'enemies', enemy)):
                for sorted_file in sorted(files, key=lambda name: name.split('.')[0]):
                    self.enemy_frames[enemy].append(pygame.image.load(join(path, sorted_file)).convert_alpha())

    def input(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            pos = self.gun.rect.center + self.gun.player_direction * 50
            Bullet(self.bullet_surf, pos, self.gun.player_direction, (self.all_sprites, self.bullet_sprites))
            self.can_shoot = False
            self.shot_time = pygame.time.get_ticks()

    def gun_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shot_time >= self.gun_cooldown:
                self.can_shoot = True

    def spawn_enemy(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.enemy_spawn_time >= self.enemy_spawn_cooldown:
            enemy = self.enemies[randint(0, len(self.enemies)-1)]
            Enemy(self.enemy_frames[enemy], self.player, (self.all_sprites, self.enemy_sprites), self.collision_sprites)
            self.enemy_spawn_time = pygame.time.get_ticks()

    def setup(self):
        map = load_pygame(join('data', 'maps', 'world.tmx'))
        for x, y, image, in map.get_layer_by_name('Ground').tiles():
            Sprite((x*TILE_SIZE, y*TILE_SIZE), image, self.all_sprites)

        for obj in map.get_layer_by_name('Objects'):
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))

        for obj in map.get_layer_by_name('Collisions'):
            CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)

        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites)
                self.gun = Gun(self.player, self.all_sprites)

        for path, dirs, files in walk(join('images', 'enemies')):
            for enemy in dirs:
                self.enemies.append(enemy)


    def run(self):
        while self.running:
            dt = self.clock.tick(144) / 1000

            # events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # updates
            self.input()
            self.all_sprites.update(dt)
            self.gun_timer()
            self.spawn_enemy()

            # render
            self.screen.fill('black')
            self.all_sprites.draw(self.player.rect.center)

            pygame.display.update()
        pygame.quit()

if __name__ == '__main__':
    g = Game()
    g.run()