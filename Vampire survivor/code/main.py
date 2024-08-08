from settings import *
from player import Player
from sprites import *
from random import randint, choice
from pytmx.util_pygame import load_pygame
from groups import AllSprites

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
        self.enemies = list(walk(join('images', 'enemies')))[0][1]
        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event, 300)
        self.spawn_positions = []
        self.enemy_frames = {}

        # sounds
        self.music = pygame.mixer.Sound(join('audio', 'music.wav'))
        self.gun_sound = pygame.mixer.Sound(join('audio', 'shoot.wav'))
        self.hit_sound = pygame.mixer.Sound(join('audio', 'impact.ogg'))

        # setup
        self.setup()
        self.load_images()

    def load_images(self):
        self.bullet_surf = pygame.image.load(join('images', 'gun', 'bullet.png')).convert_alpha()

        for enemy in self.enemies:
            self.enemy_frames[enemy] = []
            for path, _, files in walk(join('images', 'enemies', enemy)):
                for sorted_file in sorted(files, key=lambda name: name.split('.')[0]):
                    self.enemy_frames[enemy].append(pygame.image.load(join(path, sorted_file)).convert_alpha())

    def input(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            pos = self.gun.rect.center + self.gun.player_direction * 50
            self.gun_sound.play()
            Bullet(self.bullet_surf, pos, self.gun.player_direction, (self.all_sprites, self.bullet_sprites), self.enemy_sprites, self.hit_sound)
            self.can_shoot = False
            self.shot_time = pygame.time.get_ticks()

    def gun_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shot_time >= self.gun_cooldown:
                self.can_shoot = True

    def setup(self):
        map = load_pygame(join('data', 'maps', 'world.tmx'))
        self.music.play()

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
            else:
                self.spawn_positions.append((obj.x, obj.y))

    def run(self):
        while self.running:
            dt = self.clock.tick(144) / 1000

            # events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == self.enemy_event:
                    Enemy(choice(self.spawn_positions), self.enemy_frames[choice(self.enemies)], (self.all_sprites, self.enemy_sprites), self.player, self.collision_sprites)

            # updates
            self.input()
            self.all_sprites.update(dt)
            self.gun_timer()

            # render
            self.screen.fill('black')
            self.all_sprites.draw(self.player.rect.center)

            pygame.display.update()
        pygame.quit()

if __name__ == '__main__':
    g = Game()
    g.run()