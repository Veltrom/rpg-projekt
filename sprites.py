import pygame as pg
from settings import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # Alustab mängija objekti
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.vec = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE

    def get_keys(self):
        # Kontrollib klahvivajutusi
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y = -PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y = PLAYER_SPEED
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071

    def move(self, dx=0, dy=0):
        # Mängija liikumine
        if not self.collide_with_wall(dx, dy):
            self.x += dx
            self.y += dy

    def collide_with_wall(self, dir):
        # Kontrollib mängija põrkumist seinaga
        if dir == "x":
            hits = pg.sprite.spritecollide(self, self.game.bushes, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == "y":
            hits = pg.sprite.spritecollide(self, self.game.bushes, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y


    def update(self):
        # Uuendab mängija positsiooni ja kontrollib kokkupõrkeid
        self.get_keys()
        self.pos += self.vel * self.game.dt
        self.rect.x = self.pos.x
        self.collide_with_wall("x")
        self.rect.y = self.pos.y
        self.collide_with_wall("y")


class Bush(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # Alustab seina objekti
        self.groups = game.all_sprites, game.bushes
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.bush_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Grass(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # Alustab muruplatside objekti
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.grass_img
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE