import os
from random import randint
import pygame
from level import Level
from gameloop import GameLoop
from event_queue import EventQueue
from renderer import Renderer
from clock import Clock

N = 70
W = 110

LEVEL_MAP = []
for i in range(0, N):
    LEVEL_MAP.append([])
    for j in range(0, W):
        if j == 0 or j == (W-1) or i == 0 or i == (N-1):
            LEVEL_MAP[i].append(2)
        else:
            LEVEL_MAP[i].append(0)


LEVEL_MAP[int(N-N/5)][int(W/2)] = 1

for i in range(0, 6):
    x = randint(10, 25)
    y = randint(15, 55)
    LEVEL_MAP[int(x)][int(y)] = 3


CELL_SIZE = 10


def main():
    """initializes most of the things needed for the game considering the classes needed for
    the game to run and pygame-window.
    """
    height = len(LEVEL_MAP)
    width = len(LEVEL_MAP[0])
    display_height = height * CELL_SIZE
    display_width = width * CELL_SIZE

    dirname = os.path.dirname(__file__)
    background = pygame.image.load(os.path.join(dirname, "assets", "bg.png"))

    game_parameters = inquire_parameters()

    display = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption("Game")
    level = Level(LEVEL_MAP, CELL_SIZE, game_parameters[0], game_parameters[1])
    event_queue = EventQueue()
    renderer = Renderer(display, level, background)
    clock = Clock()
    game_loop = GameLoop(level, renderer, event_queue, clock, CELL_SIZE)

    pygame.init()
    game_loop.start()

def inquire_parameters():
    """Asks the user for parameters for the game. User can affect difficulty and sounds on/off
    Returns:
        level_difficulty and sounds_on_off
    """
    print("The game is starting, you will be asked for a few choices.")
    print("There are 3 different difficulties: hard, medium, easy")
    questionstring = "Please enter the difficulty you desire:\n 1 = Hard, 2 = medium, 3 = easy\n"
    try:
        level_difficulty = int(input(questionstring))
    except ValueError:
        level_difficulty = -1
    if level_difficulty not in [1, 2, 3]:
        level_difficulty = 2
        print("improper input, medium was chosen as default")
    try:
        sounds_on_off = int(input("Do you want to play with sounds on? 1 = yes, 0 = no\n"))
    except ValueError:
        sounds_on_off = -1
    if sounds_on_off not in [0, 1]:
        sounds_on_off = 0
        print("improper input, sounds off was chosen as default")
    return level_difficulty, sounds_on_off


if __name__ == "__main__":
    main()
