################################################
# Programmeerimine I
# 2024/2025 sügissemester
#
# Projekt
# Teema: RPG mäng Kaarsillast Deltani nimega "Põnni seiklused"
#
#
# Autorid: Kirke Kabonen, Kevin Peekmann
#
# mõningane eeskuju: Pokemon mängud
#
# Lisakommentaar (nt käivitusjuhend):
#
##################################################

import sys
from os import path
from sprites import *


class Game:
    def __init__(self):
        # Pygame'i alustus ning andmete laadimine
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(200, 100)
        self.load_data()

    def load_data(self):
        # Kõikide piltide laadimine
        game_folder = path.dirname(__file__)
        self.map_data = []
        img_folder = path.join(game_folder, 'img')
        with open(path.join(game_folder, 'map.txt'), encoding="utf-8") as f:
            for line in f:
                self.map_data.append(line.strip())
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.player_img = pg.transform.scale(self.player_img, (TILESIZE, TILESIZE))
        self.grass_img = pg.image.load(path.join(img_folder, MURU_IMG)). convert_alpha()
        self.grass_img = pg.transform.scale(self.grass_img, (TILESIZE, TILESIZE))
        self.bush_img = pg.image.load(path.join(img_folder, POOSAS_IMG)).convert_alpha()
        self.bush_img = pg.transform.scale(self.bush_img, (TILESIZE, TILESIZE))
        self.img_folder = path.join(path.dirname(__file__), "img")

    def new(self):
        # Alustab uue mängu ning vaatab, mis platsid on seinad
        self.all_sprites = pg.sprite.Group()
        self.bushes = pg.sprite.Group()
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == "1":
                    Bush(self, col, row)
                if tile == "P":
                    self.player = Player(self, col, row)
                if tile == ".":
                    Grass(self, col, row)

    def run(self):
        # Käivitab mängu
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        self.all_sprites.update()

    def draw(self):
        #
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def events(self):
        # Kontrollib, millal mäng kinni panna
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

g = Game()
while True:
    g.new()
    g.run()