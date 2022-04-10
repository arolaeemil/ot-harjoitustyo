import os
from random import randint
import pygame
from level import Level
from gameloop import GameLoop
from event_queue import EventQueue
from renderer import Renderer
from clock import Clock

# LEVEL_MAP = [[0, 0, 0, 0, 0],
#[0, 0, 0, 0, 0],
#[0, 0, 0, 0, 0],
# [0, 0, 1, 0, 0]]

N = 70

LEVEL_MAP = []
for i in range(0, N):
    LEVEL_MAP.append([])
    for j in range(0, N):
        if j == 0 or j == (N-1) or i == 0 or i == (N-1):
            LEVEL_MAP[i].append(2)
        else:
            LEVEL_MAP[i].append(0)


LEVEL_MAP[int(N-N/5)][int(N/2)] = 1

for i in range(0, 6):
    x = randint(10, 25)
    y = randint(15, 55)
    LEVEL_MAP[int(x)][int(y)] = 3

# print(LEVEL_MAP)


CELL_SIZE = 10


def main():
    height = len(LEVEL_MAP)
    width = len(LEVEL_MAP[0])
    display_height = height * CELL_SIZE
    display_width = width * CELL_SIZE

    dirname = os.path.dirname(__file__)
    background = pygame.image.load(os.path.join(dirname, "assets", "bg.png"))

    # window
    display = pygame.display.set_mode((display_width, display_height))

    pygame.display.set_caption("Game")

    level = Level(LEVEL_MAP, CELL_SIZE)
    event_queue = EventQueue()
    renderer = Renderer(display, level, background)
    clock = Clock()
    game_loop = GameLoop(level, renderer, event_queue, clock, CELL_SIZE)

    pygame.init()
    game_loop.start()


if __name__ == "__main__":
    main()
