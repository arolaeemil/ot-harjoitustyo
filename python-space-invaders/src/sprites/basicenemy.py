import os
from random import choice, randint
import pygame

# path to get the file
dirname = os.path.dirname(__file__)

# sprite class is inherited


class Basicenemy(pygame.sprite.Sprite):
    def __init__(self, x_coord=0, y_coord=0, what_type=1):
        # constructor call
        super().__init__()
        # type
        self.what_type = what_type
        # getting the image for the ship
        if self.what_type == 1:
            self.image = pygame.image.load(
                os.path.join(dirname, "..", "assets", "basicenemy.png"))
        if self.what_type == 2:
            self.image = pygame.image.load(
                os.path.join(dirname, "..", "assets", "basicenemy2.png"))
        # rectacular shape (50x50)
        self.rect = self.image.get_rect()
        # for fire cooldown
        self.previous_move_time = 0
        self.previous_shot_time = 0
        # starting x- and y-coordinates
        self.rect.x = x_coord
        self.rect.y = y_coord
        if self.what_type == 1:
            self.movespeed_x = choice([-2, -1, 1, 2])
            self.movespeed_y = 0
        if self.what_type == 2:
            self.movespeed_x = choice([-2, -1, 1, 2])
            self.movespeed_y = choice([-1, 1])

    def give_coords(self):
        return (self.rect.x, self.rect.y)

    def can_shoot(self, current_time):
        if self.what_type == 2:
            return False
        new_timer = randint(1, 10)*4000
        return current_time - self.previous_shot_time >= new_timer

    def should_move(self, current_time):
        return current_time - self.previous_move_time >= 30
