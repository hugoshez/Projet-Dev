import os
import pygame as pg
import settings as s
import sprites
import mobs
import random
import sqlite3
import page_fdp as show_fdp

def update_score(username, scores):
    db = sqlite3.connect("users.db")
    cursor = db.cursor()
    cursor.execute("UPDATE users SET scores = ? WHERE username = ?", (scores, username))
    db.commit()


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

        # Spawn des joueurs
        player_spawn_x = 200  # Position X du joueur 1
        player_spawn_y = 100  # Position Y du joueur 1
        player2_spawn_x = s.WIDTH - 200  # Position X du joueur 2 (sur l'autre côté de l'écran)
        player2_spawn_y = 1000  # Position Y du joueur 2
        self.player = mobs.Player(self, (player_spawn_x, player_spawn_y))
        self.player2 = mobs.Player2(self, (player2_spawn_x, player2_spawn_y))

        # Spawner un pistolet aléatoirement
        pistol_spawn_x = random.randint(0, s.WIDTH)
        pistol_spawn_y = random.randint(0, s.HEIGHT)
        pistol = sprites.Pistol(self, True)
        pistol.rect.x = pistol_spawn_x
        pistol.rect.y = pistol_spawn_y

        self.run()


    def run(self):
        # game loop
        self.playing = True
        self.counter = 10
        pg.time.set_timer(pg.USEREVENT, 1000)

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
                if event.key == pg.K_F11:
                    if self.screen.get_flags() & pg.FULLSCREEN:
                        pg.display.set_mode((s.WIDTH, s.HEIGHT), s.FLAGS)
                    else:
                        pg.display.set_mode((s.WIDTH, s.HEIGHT), s.FLAGS | pg.FULLSCREEN)
                elif event.key == pg.K_t:
                    print(str(self.clock.get_fps()))
            elif event.type == pg.USEREVENT: 
                self.counter -= 1
                if self.counter == 0:
                    if self.level_number < 3:
                        self.level_number += 1
                        self.counter = 10
                        self.new()
                    elif self.level_number == 3:
                        #fermer la fenetre principale
                        os.system('python3 page_fdp.py')
                        self.playing = False
                        self.running = False
                        print("Fin de partie")
                        os.system('python3 page_fdp.py')
                        print("Fin de jeu")


    def draw(self):
        pg.display.set_caption(s.TITLE + str(self.clock.get_fps()))
        # game loop - draw/ render
        self.screen.fill(s.BLACK)
        self.all_sprites.draw(self.screen)
        

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        # Création de la table si elle n'existe pas (avec la colonne scores)
        names = cursor.execute('''SELECT username FROM users WHERE scores = 0''').fetchall()


        # Affichage des noms des joueurs
        font = pg.font.Font(None, 36)
        player1_text = font.render(str(list(names)[-2][0]), True, s.WHITE)
        player2_text = font.render(str(list(names)[-1][0]), True, s.WHITE)
        self.screen.blit(player1_text, (10, 10))
        self.screen.blit(player2_text, (s.WIDTH - player2_text.get_width() - 10, 10))

        # Affichage du numéro du niveau
        level_text = font.render(f"Level: {self.level_number} | Timer : {self.counter}", True, s.WHITE)
        self.screen.blit(level_text, (10, 50))  


        # *after* drawing everything, flip the display
        pg.display.flip()



g = Game()
while g.running:
    g.new()
    g.level_number += 1 
    print(g.player.kill)
    print(g.level_number)
    if g.level_number == 4:
        show_fdp.show_fdp()
        g.running = False

pg.quit()