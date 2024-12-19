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
# Vajalik on pygame-ce ja pytmx
##################################################

import pygame
import os
from settings import *
from pytmx.util_pygame import load_pygame
from os.path import join

from sprites import Sprite, MonsterPatchSprite, BorderSprite, CollidableSprite
from entities import Player
from groups import AllSprites
from support import *

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Põnni seiklused')
        self.clock = pygame.time.Clock()

        # grupid
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.monster_sprites = pygame.sprite.Group()

        self.import_assets()
        self.setup(self.tmx_maps['world'], 'auh')

        self.start_time = pygame.time.get_ticks()
        self.elapsed_time = 0.0
        self.timer_font = pygame.font.SysFont(None, 30)

    def import_assets(self):
        # Laadida Tiled map
        self.tmx_maps = {
            'world': load_pygame(join('..', 'data', 'maps', 'map.tmx')),
        }

        characters_path = join('..', 'graphics', 'characters')

        # Tegelaste import
        try:
            self.overworld_frames = {
                'characters': all_character_import(characters_path)
            }
        except FileNotFoundError:
            print("Some character sprite sheets were not found. Skipping them.")
            self.overworld_frames = {'characters': {}}

        # Mängija animatsioonide laadimine
        player_path = join('..', 'graphics', 'characters', 'player')

        if os.path.exists(player_path):
            self.overworld_frames['characters']['player'] = import_sub_folders(player_path)
        else:
            print("Player animation folder not found.")
            self.overworld_frames['characters']['player'] = {}

    def setup(self, tmx_map, player_start_pos):
        # Tegelaste layeri silumine
        entities_layer = tmx_map.get_layer_by_name('Entities')
        print("Entities in the layer:")
        for obj in entities_layer:
            print(f"Object at ({obj.x}, {obj.y}) - Name: {obj.name}, Properties: {obj.properties}")

        # Kõik tausta tile'ide laadimine
        for layer in ['muru', 'mullatee', 'props', 'jõgi', 'kaarsild']:
            layer_data = tmx_map.get_layer_by_name(layer)
            for x, y, surf in layer_data.tiles():
                Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites, WORLD_LAYERS['bg'])

        # Kõikide objektide laadimine
        objects_layer = tmx_map.get_layer_by_name('Objektid')
        for obj in objects_layer:
            CollidableSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))

        #Kõik Collisionite koordinaadid, kuhu mängijal võimalik kokku põrgata
        for obj in tmx_map.get_layer_by_name('Collisions'):
            BorderSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)

        # Kõik vastased
        for obj in tmx_map.get_layer_by_name('Monsters'):
            CollidableSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites, self.monster_sprites))

        # Mängija
        entities_layer = tmx_map.get_layer_by_name('Entities')
        for obj in entities_layer:
            if obj.name == 'Player':
                if obj.properties['pos'] == player_start_pos:
                    self.player = Player(
                        pos=(obj.x, obj.y),
                        frames=self.overworld_frames['characters']['player'],
                        groups=self.all_sprites,
                        facing_direction=obj.properties['direction'],
                        collision_sprites = self.collision_sprites
                    )

        finish_layer = tmx_map.get_layer_by_name('Delta')
        for obj in finish_layer:
            self.delta_object = CollidableSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)

    def draw_timer(self):
        current_time = pygame.time.get_ticks()
        self.elapsed_time = (current_time - self.start_time) / 1000
        timer_text = f"Aeg: {self.elapsed_time:.3f}"
        timer_surface = self.timer_font.render(timer_text, True, (255, 255, 255))
        self.display_surface.blit(timer_surface, (10, 10))

    def fade_to_black(self, color=(0, 0, 0)):
        fade_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        fade_surface.fill(color)
        for alpha in range(0, 255, 5):
            fade_surface.set_alpha(alpha)
            self.display_surface.fill('black')
            self.all_sprites.draw(self.player.rect.center)
            self.display_surface.blit(fade_surface, (0, 0))
            pygame.display.update()
            self.clock.tick(60)

    def display_message(self, message, duration, color=(255, 255, 255)):
        font = pygame.font.Font(None, 50)
        lines = message.split('\n')
        line_surfaces = [font.render(line, True, color) for line in lines]
        line_rects = [line.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + i * 60))
                      for i, line in enumerate(line_surfaces)]

        end_time = pygame.time.get_ticks() + duration * 1000
        while pygame.time.get_ticks() < end_time:
            self.display_surface.fill('black')
            for surface, rect in zip(line_surfaces, line_rects):
                self.display_surface.blit(surface, rect)
            pygame.display.update()
            self.clock.tick(60)

    def check_monster_collision(self):
        if pygame.sprite.spritecollide(self.player, self.monster_sprites, False):
            self.fade_to_black()
            self.display_message("Surid deemonkassile!", 5, color=(255, 0, 0))
            pygame.quit()
            exit()

    def lopp_staatus(self):
        if pygame.sprite.collide_rect(self.player, self.delta_object):
            final_time = self.elapsed_time
            self.fade_to_black()
            message = f"Palju õnne, jõudsid turvaliselt Deltasse!\nLõppaeg: {final_time:.3f}"
            self.display_message(message, 6)
            pygame.quit()
            exit()

    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            # Mängu loop, kus kontrollib, kas mäng kinni pandud
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()

            # Mänguloogika
            self.all_sprites.update(dt)
            self.check_monster_collision()
            self.lopp_staatus()
            self.display_surface.fill('black')
            self.all_sprites.draw(self.player.rect.center)
            self.draw_timer()
            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()
