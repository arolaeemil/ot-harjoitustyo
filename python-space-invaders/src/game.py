import pygame
from level import Level
from gameloop import GameLoop
from event_queue import EventQueue
from renderer import Renderer
from clock import Clock
import os
from random import *

# LEVEL_MAP = [[0, 0, 0, 0, 0],
#[0, 0, 0, 0, 0],
#[0, 0, 0, 0, 0],
# [0, 0, 1, 0, 0]]

n = 70

LEVEL_MAP = []
for i in range(0, n):
    LEVEL_MAP.append([])
    for j in range(0, n):
        if j == 0 or j == (n-1) or i == 0 or i == (n-1):
            LEVEL_MAP[i].append(2)
        else:
            LEVEL_MAP[i].append(0)


LEVEL_MAP[int(n-n/5)][int(n/2)] = 1

for i in range(0,6):
    x = randint(10,25)
    y = randint(15,55)
    LEVEL_MAP[int(x)][int(y)] = 3

# print(LEVEL_MAP)


CELL_SIZE = 10


def main():
    height = len(LEVEL_MAP)
    width = len(LEVEL_MAP[0])
    display_height = height * CELL_SIZE
    display_width = width * CELL_SIZE

    dirname = os.path.dirname(__file__)
    bg = pygame.image.load(os.path.join(dirname, "assets", "bg.png"))

    # window
    display = pygame.display.set_mode((display_width, display_height))

    pygame.display.set_caption("Game")

    level = Level(LEVEL_MAP, CELL_SIZE)
    event_queue = EventQueue()
    renderer = Renderer(display, level, bg)
    clock = Clock()
    game_loop = GameLoop(level, renderer, event_queue, clock, CELL_SIZE)

    pygame.init()
    game_loop.start()


if __name__ == "__main__":
    main()
