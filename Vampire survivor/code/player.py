from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites) -> None:
        super().__init__(groups)
        self.load_images()
        self.state = 'down'
        self.frame_index = 0
        self.image = pygame.image.load(join('images', 'player', 'down', '0.png'))
        self.rect = self.image.get_frect(center = pos)
        self.hitbox = self.rect.inflate(-30, -90)

        # movement
        self.direction = Vector2()
        self.speed = 400
        self.collision_sprites = collision_sprites

    def input(self):
        keys = pygame.key.get_pressed()
        recent_keys = pygame.key.get_just_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.hitbox.right = sprite.rect.left
                    if self.direction.x < 0: self.hitbox.left = sprite.rect.right
                else:
                    if self.direction.y > 0: self.hitbox.bottom = sprite.rect.top
                    if self.direction.y < 0: self.hitbox.top = sprite.rect.bottom

    def move(self, dt):
        self.hitbox.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * self.speed * dt
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def animate(self, dt):
        # get state
        if self.direction.x != 0:
            self.state = 'right' if self.direction.x > 0 else 'left'
        if self.direction.y != 0:
            self.state = 'down' if self.direction.y > 0 else 'up'

        # animate
        self.frame_index = self.frame_index + 5 * dt if self.direction else 0
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]

    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)

    def load_images(self):
        self.frames = {'left': [],'right': [],'up': [],'down': []}

        for state in self.frames:
            for path, dirs, files in walk(join('images', 'player', state)):
                if files:
                    for file in sorted(files, key=lambda name: int(name.split('.')[0])):
                        surf = pygame.image.load(join(path, file)).convert_alpha()
                        self.frames[state].append(surf)