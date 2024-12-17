import pygame
import os
from settings import *
from pytmx.util_pygame import load_pygame
from os.path import join

from sprites import Sprite
from entities import Player, Character
from groups import AllSprites
from support import *

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Põnni seiklused')
        self.clock = pygame.time.Clock()

        # groups 
        self.all_sprites = AllSprites()

        self.import_assets()
        self.setup(self.tmx_maps['world'], 'house')

    def import_assets(self):
        # Load Tiled map
        self.tmx_maps = {
            'world': load_pygame(join('..', 'data', 'maps', 'world.tmx')),
        }

        characters_path = join('..', 'graphics', 'characters')

        # General characters import (from sprite sheets)
        try:
            self.overworld_frames = {
                'characters': all_character_import(characters_path)
            }
        except FileNotFoundError:
            print("Some character sprite sheets were not found. Skipping them.")
            self.overworld_frames = {'characters': {}}

        # Load player-specific animations (should have subfolders for each direction and idle)
        player_path = join('..', 'graphics', 'characters', 'player')
        if os.path.exists(player_path):
            # This will create a dictionary like:
            # {
            #   'up': [...],
            #   'down': [...],
            #   'left': [...],
            #   'right': [...],
            #   'up_idle': [...],
            #   'down_idle': [...],
            #   'left_idle': [...],
            #   'right_idle': [...]
            # }
            self.overworld_frames['characters']['player'] = import_sub_folders(player_path)
        else:
            print("Player animation folder not found.")
            self.overworld_frames['characters']['player'] = {}

    def setup(self, tmx_map, player_start_pos):
        # Terrain layers
        for layer in ['Terrain', 'Terrain Top']:
            layer_data = tmx_map.get_layer_by_name(layer)
            for x, y, surf in layer_data.tiles():
                Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites)

        # Objects 
        objects_layer = tmx_map.get_layer_by_name('Objects')
        for obj in objects_layer:
            Sprite((obj.x, obj.y), obj.image, self.all_sprites)

        # Entities 
        entities_layer = tmx_map.get_layer_by_name('Entities')
        for obj in entities_layer:
            if obj.name == 'Player':
                # Only create the player if positions match the start_pos condition
                if obj.properties['pos'] == player_start_pos:
                    self.player = Player(
                        pos=(obj.x, obj.y),
                        frames=self.overworld_frames['characters']['player'],
                        groups=self.all_sprites,
                        facing_direction=obj.properties['direction']
                    )
            else:
                Character(
                    pos=(obj.x, obj.y),
                    frames=self.overworld_frames['characters'][obj.properties['graphic']],
                    groups=self.all_sprites,
                    facing_direction=obj.properties['direction']
                )

    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            # event loop 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # game logic 
            self.all_sprites.update(dt)
            self.display_surface.fill('black')
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()
