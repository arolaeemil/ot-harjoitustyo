import os
import pygame

dirname = os.path.dirname(__file__)

class Blocker(pygame.sprite.Sprite):
    def __init__(self, x_coord=0, y_coord=0):
        super().__init__()

        self.image = pygame.image.load(os.path.join(
            dirname, "..", "assets", "block.png"))

        self.rect = self.image.get_rect()

        self.rect.x = x_coord
        self.rect.y = y_coord
