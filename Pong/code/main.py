from settings import *
from sprites import *

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

        # sprites
        self.all_sprites = pg.sprite.Group()
        self.paddle_sprites = pg.sprite.Group()

        self.player = Player((self.all_sprites, self.paddle_sprites))
        self.ball = Ball(self.all_sprites, self.paddle_sprites, self.update_score)
        self.opponent = Opponnent((self.all_sprites, self.paddle_sprites), self.ball)

        # score
        self.score = {'player': 0, 'opponent': 0}
        self.font = pg.font.Font(None, 160)

    def display_score(self):
        # player
        player_surf = self.font.render(str(self.score['player']), True, COLORS['bg detail'])
        player_rect = player_surf.get_frect(center = (WINDOW_WIDTH / 2 + 100, WINDOW_HEIGHT / 2))
        self.screen.blit(player_surf, player_rect)

        # opponent
        opp_surf = self.font.render(str(self.score['opponent']), True, COLORS['bg detail'])
        opp_rect = opp_surf.get_frect(center = (WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 2))
        self.screen.blit(opp_surf, opp_rect)

        # line
        pg.draw.line(self.screen, COLORS['bg detail'], (WINDOW_WIDTH / 2, 0), (WINDOW_WIDTH / 2, WINDOW_HEIGHT), 8)

    def update_score(self, side):
        self.score[side] += 1

    def run(self):
        while self.running:
            dt = self.clock.tick(144) / 1000

            # events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

            # updates
            # self.input(dt)
            self.all_sprites.update(dt)

            # render
            self.screen.fill(COLORS['bg'])
            self.all_sprites.draw(self.screen)
            self.display_score()

            pg.display.update()
        pg.quit()


if __name__ == '__main__':
    g = Game()
    g.run()
