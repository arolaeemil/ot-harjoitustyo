import os
from random import choice, randint
import pygame

# path to get the file
dirname = os.path.dirname(__file__)

# sprite class is inherited


class Basicenemy(pygame.sprite.Sprite):
    def __init__(self, x_coord=0, y_coord=0):
        # constructor call
        super().__init__()

        # getting the image for the ship
        self.image = pygame.image.load(
            os.path.join(dirname, "..", "assets", "basicenemy.png"))
        # rectacular shape (50x50)
        self.rect = self.image.get_rect()
        # for fire cooldown
        self.previous_move_time = 0
        self.previous_shot_time = 0
        # starting x- and y-coordinates
        self.rect.x = x_coord
        self.rect.y = y_coord
        self.movedir = choice([-10, -9, -8, -7, -6, -5, 5, 6, 7, 8, 9, 10])/10

    def give_coords(self):
        return (self.rect.x, self.rect.y)

    def can_shoot(self, current_time):
        new_timer = randint(1, 10)*4000
        return current_time - self.previous_shot_time >= new_timer

    def should_move(self, current_time):
        return current_time - self.previous_move_time >= 30
