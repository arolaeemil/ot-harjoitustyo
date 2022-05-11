import os
from random import choice, randint
import pygame

dirname = os.path.dirname(__file__)

class Basicenemy(pygame.sprite.Sprite):
    def __init__(self, x_coord=0, y_coord=0, what_type=1):
        """normal enemies which spawn in the game, there are two types currently.
        Movespeeds have random variation.
        Args:
            x_coord (int, optional): starting x-coordinate
            y_coord (int, optional): starting y-coordinate
            what_type (int, optional): can be 1 or 2.
            Type 2 enemy move differently but doesnt shoot blobs.
        """
        super().__init__()

        self.what_type = what_type

        if self.what_type == 1:
            self.image = pygame.image.load(
                os.path.join(dirname, "..", "assets", "basicenemy.png"))
        if self.what_type == 2:
            self.image = pygame.image.load(
                os.path.join(dirname, "..", "assets", "basicenemy2.png"))
        self.rect = self.image.get_rect()

        self.previous_move_time = 0
        self.previous_shot_time = 0

        self.rect.x = x_coord
        self.rect.y = y_coord
        if self.what_type == 1:
            self.movespeed_x = choice([-2, -1, 1, 2])
            self.movespeed_y = 0
        if self.what_type == 2:
            self.movespeed_x = choice([-2, -1, 1, 2])
            self.movespeed_y = choice([-1, 1])

    def give_coords(self):
        """Gives x- and y-coordinates
        Returns:
            x-coordinate, y-coordinate
        """
        return (self.rect.x + 25, self.rect.y)

    def can_shoot(self, current_time):
        """Tells if enemy can shoot a blob
        Returns:
            True: if can shoot a blob
            False: if cannot shoot a blob yet or if is of wrong type
        """
        if self.what_type == 2:
            return False
        new_timer = randint(1, 10)*4000
        return current_time - self.previous_shot_time >= new_timer

    def should_move(self, current_time):
        """Tells if enemy should move
        Returns:
            True: if should move
            False: if should not move yet
        """
        return current_time - self.previous_move_time >= 30
