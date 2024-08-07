from settings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.offset = Vector2()

    def draw(self, target):
        self.offset.x = -(target[0] - WINDOW_WIDTH / 2)
        self.offset.y = -(target[1] - WINDOW_HEIGHT / 2)

        ground_sprites = []
        object_sprites = []
        for sprite in self:
            if hasattr(sprite, 'ground'):
                ground_sprites.append(sprite)
            else:
                object_sprites.append(sprite)

        for sprite in ground_sprites:
            self.screen.blit(sprite.image, sprite.rect.topleft + self.offset)

        for sprite in sorted(object_sprites, key=lambda sprite: sprite.rect.centery):
            self.screen.blit(sprite.image, sprite.rect.topleft + self.offset)