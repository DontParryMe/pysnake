import os
from random import choice

from code.resources import resource_path
from code.settings import *
from math import sin


class Apple:
    def __init__(self, snake):
        self.pos = pygame.Vector2()
        self.display_surface = pygame.display.get_surface()
        self.snake = snake
        self.set_pos()

        image_path = resource_path(os.path.join('graphics', 'apple.png'))
        self.surf = pygame.image.load(image_path).convert_alpha()
        self.scaled_surf = self.surf.copy()
        self.scaled_rect = self.scaled_surf.get_rect(center=(self.pos.x * CELL_SIZE + CELL_SIZE / 2,
                                                             self.pos.y * CELL_SIZE + CELL_SIZE / 2))

    def set_pos(self):
        available_pos = [pygame.Vector2(x, y) for x in range(COLS) for y in range(ROWS)
                         if pygame.Vector2(x, y) not in self.snake.body]
        self.pos = choice(available_pos)

    def draw(self):
        scale = 1 + sin(pygame.time.get_ticks() / 600) / 3
        self.scaled_surf = pygame.transform.smoothscale_by(self.surf, scale)
        self.scaled_rect = self.scaled_surf.get_rect(center=(self.pos.x * CELL_SIZE + CELL_SIZE / 2,
                                                             self.pos.y * CELL_SIZE + CELL_SIZE / 2))

        self.display_surface.blit(self.scaled_surf, self.scaled_rect)

