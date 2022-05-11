import os
from random import choice, randint
import pygame

dirname = os.path.dirname(__file__)

class Boss(pygame.sprite.Sprite):
    def __init__(self, x_coord=0, y_coord=0, what_type=1):
        """Boss entity.
        Args:
            x_coord (int, optional): starting x-coordinate
            y_coord (int, optional): starting y-coordinate
            what_type (int, optional): can be 1 at the moment. Later more bosses may be added.
        """
        super().__init__()

        self.what_type = what_type
        self.health_points = 5
        if self.what_type == 1:
            self.image = pygame.image.load(
                os.path.join(dirname, "..", "assets", "boss.png"))
        self.rect = self.image.get_rect()
        self.previous_shot_time = 0
        self.previous_move_time = 0
        self.rect.y = y_coord
        self.rect.x = x_coord
        if self.what_type == 1:
            self.movespeed_x = choice([-1,1])
            self.movespeed_y = 0

    def give_coords(self):
        """Gives x- and y-coordinates to roughly middle of the boss rectacon
        Returns:
            x-coordinate, y-coordinate
        """
        return (self.rect.x + 150, self.rect.y + 50)

    def can_shoot(self, current_time):
        """Returns True if boss can shoot
        Returns:
            True: if boss can shoot
            False if cannot shoot
        """
        new_timer = randint(1, 10)*800
        return current_time - self.previous_shot_time >= new_timer

    def should_move(self, current_time):
        """Returns True if boss can move
        Returns:
            True: if boss can move
            False if cannot move
        """
        return current_time - self.previous_move_time >= 30

    def is_kill(self):
        """return state of boss, contineus to live or dies
        Returns:
            False if hp is still above value zero
            True if hp has reached value zero
        """
        if self.health_points <= 0:
            return True
        return False

    def remove_hp(self, amount):
        """Removes health points from boss based on given amount.
        """
        self.health_points = self.health_points - amount
