import os
from os.path import join

from code.resources import resource_path
from code.settings import *
from os import walk


class Snake:
    def __init__(self):
        # setup
        self.display_surface = pygame.display.get_surface()
        self.body = [pygame.Vector2(START_COL - col, START_ROW) for col in range(START_LENGTH)]
        self.direction = pygame.Vector2(1, 0)
        self.has_eaten = False

        # graphics
        self.surfs = self.import_surfs()
        print(self.surfs)
        self.draw_data = []
        self.head_surf = self.surfs['head_right']
        self.tail_surf = self.surfs['tail_left']
        self.update_body()

    def import_surfs(self):
        surf_dict = {}
        folder_path = resource_path('graphics/snake')
        print(f'Looking in: {folder_path}')
        if not os.path.exists(folder_path):
            print(f'Path does not exist: {folder_path}')
        for _, _, image_names in walk(folder_path):
            for image_name in image_names:
                full_path = resource_path(join(folder_path, image_name))
                surface = pygame.image.load(full_path).convert_alpha()
                key_name = image_name.split('.')[0]
                surf_dict[key_name] = surface
        return surf_dict

    def update(self):
        if not self.has_eaten:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
        else:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.has_eaten = False
        self.update_head()
        self.update_tail()
        self.update_body()

    def reset(self):
        self.body = [pygame.Vector2(START_COL - col, START_ROW) for col in range(START_LENGTH)]
        self.direction = pygame.Vector2(1, 0)
        self.update_head()
        self.update_tail()
        self.update_body()

    def update_head(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == pygame.Vector2(-1, 0): self.head_surf = self.surfs['head_right']
        if head_relation == pygame.Vector2(1, 0): self.head_surf = self.surfs['head_left']
        if head_relation == pygame.Vector2(0, -1): self.head_surf = self.surfs['head_down']
        if head_relation == pygame.Vector2(0, 1): self.head_surf = self.surfs['head_up']

    def update_tail(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == pygame.Vector2(1, 0): self.tail_surf = self.surfs['tail_left']
        if tail_relation == pygame.Vector2(-1, 0): self.tail_surf = self.surfs['tail_right']
        if tail_relation == pygame.Vector2(0, 1): self.tail_surf = self.surfs['tail_up']
        if tail_relation == pygame.Vector2(0, -1): self.tail_surf = self.surfs['tail_down']

    def update_body(self):
        self.draw_data = []
        for index, part in enumerate(self.body):
            # position
            x = part.x * CELL_SIZE
            y = part.y * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            if index == 0:
                self.draw_data.append((self.head_surf, rect))
            elif index == len(self.body) - 1:
                self.draw_data.append((self.tail_surf, rect))
            else:
                last_part = self.body[index + 1] - part
                next_part = self.body[index - 1] - part
                if last_part.x == next_part.x:
                    self.draw_data.append((self.surfs['body_horizontal'], rect))
                elif last_part.y == next_part.y:
                    self.draw_data.append((self.surfs['body_vertical'], rect))
                else: # corners
                    if last_part.x == -1 and next_part.y == -1 or last_part.y == -1 and next_part.x == -1:
                        self.draw_data.append((self.surfs['body_tl'], rect))
                    if last_part.x == -1 and next_part.y == 1 or last_part.y == 1 and next_part.x == -1:
                        self.draw_data.append((self.surfs['body_bl'], rect))
                    if last_part.x == 1 and next_part.y == -1 or last_part.y == -1 and next_part.x == 1:
                        self.draw_data.append((self.surfs['body_tr'], rect))
                    if last_part.x == 1 and next_part.y == 1 or last_part.y == 1 and next_part.x == 1:
                        self.draw_data.append((self.surfs['body_br'], rect))

    def draw(self):
        for surf, rect in self.draw_data:
            self.display_surface.blit(surf, rect)
