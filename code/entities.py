import pygame
from settings import *
from pygame.math import Vector2 as vector

class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, facing_direction):
        super().__init__(groups)
        self.z = WORLD_LAYERS['main']
        # graphics 
        self.frames = frames
        self.frame_index = 0
        self.facing_direction = facing_direction

        # movement 
        self.direction = vector()
        self.speed = 250

        # initial image 
        self.image = self.frames[self.get_state()][int(self.frame_index)]
        self.rect = self.image.get_rect(center=pos)
        self.y_sort = self.rect.centery

    def animate(self, dt):
        self.frame_index += ANIMATION_SPEED * dt
        current_frames = self.frames[self.get_state()]
        self.image = current_frames[int(self.frame_index) % len(current_frames)]

    def get_state(self):
        moving = bool(self.direction.magnitude() != 0)
        if moving:
            # Update facing direction if moving horizontally
            if self.direction.x > 0:
                self.facing_direction = 'right'
            elif self.direction.x < 0:
                self.facing_direction = 'left'
            # Update facing direction if moving vertically
            if self.direction.y > 0:
                self.facing_direction = 'down'
            elif self.direction.y < 0:
                self.facing_direction = 'up'

        # If not moving, use idle
        return f'{self.facing_direction}' if moving else f'{self.facing_direction}_idle'

class Character(Entity):
    def __init__(self, pos, frames, groups, facing_direction):
        super().__init__(pos, frames, groups, facing_direction)

class Player(Entity):
    def __init__(self, pos, frames, groups, facing_direction):
        super().__init__(pos, frames, groups, facing_direction)

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = 0
        self.direction.y = 0
        if keys[pygame.K_UP]:
            self.direction.y = -1
        if keys[pygame.K_DOWN]:
            self.direction.y = 1
        if keys[pygame.K_LEFT]:
            self.direction.x = -1
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1

        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

    def move(self, dt):
        self.rect.center += self.direction * self.speed * dt

    def update(self, dt):
        self.y_sort = self.rect.centery
        self.input()
        self.move(dt)
        self.animate(dt)
