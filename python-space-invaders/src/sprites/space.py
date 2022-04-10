import pygame
import os

# path to get the file
dirname = os.path.dirname(__file__)

# sprite class is inherited


class Space(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0):
        # constructor call
        super().__init__()

        # getting the image for the ship
        self.image = pygame.image.load(os.path.join(
            dirname, "..", "assets", "space.png"))
        # rectacular shape (50x50)
        self.rect = self.image.get_rect()

        # starting x- and y-coordinates
        self.rect.x = x
        self.rect.y = y
