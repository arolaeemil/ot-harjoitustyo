import os
import unittest
import pygame
from random import randint
from level import Level
#from clock import Clock
#from renderer import Renderer
#from event_queue import EventQueue
from gameloop import GameLoop
#from sprites.basicenemy import Basicenemy
#from sprites.shot import Shot
#from sprites.blob import Blob

#Needs to think a bit how to test pygame events considering keyboard input and other features in gameloop class.

CELL_SIZE = 10

N = 70

LEVEL_MAP = []
for i in range(0, N):
    LEVEL_MAP.append([])
    for j in range(0, N):
        if j == 0 or j == (N-1) or i == 0 or i == (N-1):
            LEVEL_MAP[i].append(2)
        else:
            LEVEL_MAP[i].append(0)


LEVEL_MAP[5][5] = 1

LEVEL_MAP[10][10] = 3

# test map creation ends

class TestGameloop(unittest.TestCase):
    def setUp(self):
        #self.event_queue = EventQueue()
        events = []
        self.event_queue = StubEventQueue(events)
        height = len(LEVEL_MAP)
        width = len(LEVEL_MAP[0])
        display_height = height * CELL_SIZE
        display_width = width * CELL_SIZE
        self.display = pygame.display.set_mode((display_width, display_height))
        #self.clock = Clock()
        self.clock = StubClock()
        self.level = Level(LEVEL_MAP, CELL_SIZE)
        os.path.dirname(__file__)
        #background = pygame.image.load(os.path.join("src", "assets", "bg.png"))
        #self.renderer = Renderer(self.display, self.level, background)
        self.renderer = StubRenderer()
        self.gameloop = GameLoop(self.level, self.renderer, self.event_queue, self.clock, CELL_SIZE)
        #pass

    def test_can_handle_events_without_error(self):
        self.gameloop._handle_events()

    def test_controls(self):
        events = [StubEvent(pygame.KEYUP, pygame.K_DOWN),
            StubEvent(pygame.KEYDOWN, pygame.K_SPACE)]
        gameloop = GameLoop(self.level, StubRenderer(), StubEventQueue(events), StubClock(), CELL_SIZE)
        #gameloop.start()
        gameloop._handle_events()
        self.assertEqual(gameloop.down, False)
        self.assertEqual(gameloop.shoot, False)
        self.assertEqual(gameloop.left, False)
        self.assertEqual(gameloop.right, False)

class StubRenderer:
    def render(self):
        pass

class StubClock:
    def tick(self, fps):
        pass

    def get_ticks(self):
        return 0

class StubEvent:
    def __init__(self, event_type, key):
        self.type = event_type
        self.key = key

class StubEventQueue:
    def __init__(self, events):
        self.events = events

    def get(self):
        return self.events