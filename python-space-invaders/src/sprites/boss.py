import os
from random import choice, randint
import pygame

# path to get the file
dirname = os.path.dirname(__file__)

# sprite class is inherited

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
        self.hp = 5

        if self.what_type == 1:
            self.image = pygame.image.load(
                os.path.join(dirname, "..", "assets", "boss.png"))
        self.rect = self.image.get_rect()

        # for cooldown
        self.previous_move_time = 0
        self.previous_shot_time = 0
        # starting x- and y-coordinates
        self.rect.x = x_coord
        self.rect.y = y_coord
        if self.what_type == 1:
            self.movespeed_x = choice([-1,1])
            self.movespeed_y = 0

    def give_coords(self):
        return (self.rect.x + 150, self.rect.y + 50)

    def can_shoot(self, current_time):
        new_timer = randint(1, 10)*800
        return current_time - self.previous_shot_time >= new_timer

    def should_move(self, current_time):
        return current_time - self.previous_move_time >= 30

    def is_kill(self):
        """return state of boss, contineus to live or dies 
        Returns:
            False if hp is still above value zero
            True if hp has reached value zero
        """
        if self.hp <= 0:
            return True
        return False
    
    def remove_hp(self, amount):
        self.hp = self.hp - amount
