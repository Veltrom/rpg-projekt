import os
from os import path
import pygame as pg
from settings import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(0, 0, TILESIZE, TILESIZE)
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0, 0)
        
        self.animations = self.load_animations()
        self.standing_frames = {
            "up": self.animations["up"][1],    # Esimene kaader "üles" suuna jaoks
            "down": pg.transform.scale(pg.image.load(path.join(self.game.img_folder, "kass_idle.png")).convert_alpha(), (TILESIZE, TILESIZE)),
            "left": self.animations["left"][1],
            "right": self.animations["right"][1],
        }
        
        
        self.current_frame = 0
        self.last_update = 0
        self.direction = "down"
        self.image = self.standing_frames[self.direction]


    def load_animations(self):
        animations = {}
        for direction, files in PLAYER_ANIMATIONS.items():
            frames = [pg.image.load(path.join(self.game.img_folder, file)).convert_alpha() for file in files]
            animations[direction] = [pg.transform.scale(frame, (TILESIZE, TILESIZE)) for frame in frames]
        return animations


    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0 or self.vel.y != 0:  # Kui mängija liigub
            if now - self.last_update > 150:  # Muuda kaader iga 150ms järel
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.animations[self.direction])
                self.image = self.animations[self.direction][self.current_frame]
        else:  # Kui mängija ei liigu
            self.image = self.standing_frames[self.direction]



    def get_keys(self):
        # Kontrollib klahvivajutusi
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -PLAYER_SPEED
            self.direction = "left"
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = PLAYER_SPEED
            self.direction = "right"
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y = -PLAYER_SPEED
            self.direction = "up"
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y = PLAYER_SPEED
            self.direction = "down"
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
        self.animate()  # Lisa animatsiooni uuendamine


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