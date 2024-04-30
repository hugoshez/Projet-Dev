import os
import pygame as pg
import settings as s
import sprites
import mobs




class Game:
    def __init__(self):
        # initialize game, pg and create window
        self.running = True
        pg.init()
        self.screen = pg.display.set_mode((s.WIDTH, s.HEIGHT), s.FLAGS | pg.FULLSCREEN)
        pg.display.set_caption(s.TITLE)
        self.clock = pg.time.Clock()
        self.playing = True
        self.all_events = pg.event.get()
        pg.event.set_allowed(s.ALLOWED_EVENTS)

        # using ordered updates so player will rendered last (on top)
        self.all_sprites = pg.sprite.OrderedUpdates()
        self.map = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.player = None
        self.level_number = 1  # Variable pour le numéro de niveau
        

    def new(self):
        # start new game
        # SPRITE GROUPS
        # using ordered updates so player will rendered last (on top)
        self.all_sprites = pg.sprite.OrderedUpdates()
        self.map = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.enemies = pg.sprite.Group()

        # OBJECTS
        level_filename = f"level{self.level_number}.txt"  # Nom du fichier de niveau à charger
        l = sprites.Level(self, os.path.join(s.map_folder, level_filename), 60, 34)  # Charger le niveau
        l.build()

        pistol1 = sprites.Pistol(self, False)
        pistol3 = sprites.Pistol(self, True)

        self.player = mobs.Player(self, (500, 700))
        pistol3.rect.x = 200
        pistol3.rect.y = 800

        self.player2 = mobs.Player2(self, (600, 700))
        pistol3.rect.x = 200
        pistol3.rect.y = 800
        # ADD TO SPRITE GROUP IN RIGHT ORDER, init player last

        # run game AFTER everything is set up
        self.run()


    def run(self):
        # game loop
        self.playing = True
        while self.playing:
            self.clock.tick(s.FPS)
            self.handle_events()
            self.update()
            self.draw()

    def update(self):
        # game loop - update
        self.all_sprites.update()
        # collision detected by sprites

    def handle_events(self):
        # game loop - events
        # sprites do event handling their selves, they iterate through self.all_events
        self.all_events = pg.event.get()
        for event in self.all_events:
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    if self.playing:
                        self.playing = False
                    self.running = False
                elif event.key == pg.K_F11:
                    if self.screen.get_flags() & pg.FULLSCREEN:
                        pg.display.set_mode((s.WIDTH, s.HEIGHT), s.FLAGS)
                    else:
                        pg.display.set_mode((s.WIDTH, s.HEIGHT), s.FLAGS | pg.FULLSCREEN)
                elif event.key == pg.K_t:
                    print(str(self.clock.get_fps()))

    def draw(self):
        pg.display.set_caption(s.TITLE + str(self.clock.get_fps()))
        # game loop - draw/ render
        self.screen.fill(s.BLACK)
        self.all_sprites.draw(self.screen)


        # Affichage des noms des joueurs
        font = pg.font.Font(None, 36)
        player1_text = font.render("Player 1", True, s.WHITE)
        player2_text = font.render("Player 2", True, s.WHITE)
        self.screen.blit(player1_text, (10, 10))
        self.screen.blit(player2_text, (s.WIDTH - player2_text.get_width() - 10, 10))

        # Affichage du numéro du niveau
        level_text = font.render(f"Level: {self.level_number}", True, s.WHITE)
        self.screen.blit(level_text, (10, 50))  


        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # show splash/ start screen
        pass

    def show_go_screen(self):
        # show game over screen
        pass

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.level_number += 1  # Passage au niveau suivant
    g.show_go_screen()

pg.quit()
