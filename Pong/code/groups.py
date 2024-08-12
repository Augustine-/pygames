from settings import *

class AllSprites(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pg.display.get_surface()

    def draw(self):
        for sprite in self:
            for i in range(5):
                self.display_surface.blit(sprite.shadow_surf, sprite.rect.topleft + Vector2(i, i))

        for sprite in self:
            self.display_surface.blit(sprite.image, sprite.rect)

