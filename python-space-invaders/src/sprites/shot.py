import pygame
import os

# path to get the file
dirname = os.path.dirname(__file__)

# sprite class is inherited


class Shot(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0):
        # constructor call
        super().__init__()
        self.previous_move_time = 0

        # getting the image for the ship
        self.image = pygame.image.load(os.path.join(
            dirname, "..", "assets", "missile.png"))
        # rectacular shape (50x50)
        self.rect = self.image.get_rect()

        # starting x- and y-coordinates
        self.rect.x = x
        self.rect.y = y

    def should_move(self, current_time):
        return current_time - self.previous_move_time >= 30

    def give_coords(self):
        return (self.rect.x, self.rect.y)
