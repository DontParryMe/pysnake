import pygame
from sys import exit
from os.path import join

CELL_SIZE = 80
ROWS = 10
COLS = 16
WINDOW_WIDTH = COLS * CELL_SIZE
WINDOW_HEIGHT = ROWS * CELL_SIZE

# colors
GREY = 'grey'
LIGHT_GREY = '#d3d3d3'

# start_pos
START_LENGTH = 3
START_ROW = ROWS / 2
START_COL = START_LENGTH

# shadow
SHADOW_SIZE = pygame.Vector2(4, 4)
SHADOW_OPACITY = 50
