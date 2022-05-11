import unittest
from unittest import mock
import pygame
from game import main, inquire_parameters

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

class TestGame(unittest.TestCase):
    def test_setUp(self):
        self.test_help = None
    
    def test_inquire_parameters(self):
        with mock.patch('builtins.input', side_effect=[1, 0]):
            difficulty, sounds = inquire_parameters()
        self.assertEqual(difficulty, 1)
        self.assertEqual(sounds, 0)

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
