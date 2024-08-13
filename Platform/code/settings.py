import pygame as pg
from os import walk
from os.path import join
from pytmx.util_pygame import load_pygame
from pygame import Vector2

WINDOW_WIDTH, WINDOW_HEIGHT = 1280,720
WINDOW_CENTER = Vector2(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
TILE_SIZE = 64
FRAMERATE = 60
BG_COLOR = '#fcdfcd'


