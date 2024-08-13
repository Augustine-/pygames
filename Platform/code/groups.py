from settings import *

from settings import *

class AllSprites(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen = pg.display.get_surface()
        self.offset = Vector2()

    def draw(self, target):
        self.offset.x = -(target[0] - WINDOW_WIDTH / 2)
        self.offset.y = -(target[1] - WINDOW_HEIGHT / 2)

        for sprite in self:
            self.screen.blit(sprite.image, sprite.rect.topleft + self.offset)
