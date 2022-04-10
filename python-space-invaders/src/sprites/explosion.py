import pygame
import os

# path to get the file
dirname = os.path.dirname(__file__)

# sprite class is inherited


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0, current_time=0):
        # constructor call
        super().__init__()

        # getting the image for the ship
        self.image = pygame.image.load(
            os.path.join(dirname, "..", "assets", "explosion.png"))
        # rectacular shape (50x50)
        self.rect = self.image.get_rect()
        # for fire cooldown
        # starting x- and y-coordinates
        self.rect.x = x
        self.rect.y = y
        self.birth_time = current_time

    def give_coords(self):
        return (self.rect.x, self.rect.y)

    def can_fade(self, current_time):
        return current_time - self.birth_time >= 1500