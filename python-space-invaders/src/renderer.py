import pygame


class Renderer:
    def __init__(self, display, level, bg):
        self._display = display
        self._level = level
        self._bg = bg

    def render(self):
        self._display.blit(self._bg, (0, 0))
        self._level.all_sprites.draw(self._display)

        pygame.display.update()