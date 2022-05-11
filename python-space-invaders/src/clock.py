import pygame


class Clock:
    def __init__(self):
        self._clock = pygame.time.Clock()

    def tick(self, fps):
        """ticks the clock forward
        """
        self._clock.tick(fps)

    def get_ticks(self):
        """returns clock tick
        Returns:
            clock ticks
        """
        return pygame.time.get_ticks()
