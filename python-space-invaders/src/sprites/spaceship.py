import os
import pygame

dirname = os.path.dirname(__file__)

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x_coord=0, y_coord=0):
        """player ship, also holds paths to sounds related to its own actions.
        Args:
            x_coord (int, optional): starting x-coordinate
            y_coord (int, optional): starting y-coordinate
        """
        super().__init__()

        self.image = pygame.image.load(
            os.path.join(dirname, "..", "assets", "ship.png"))

        self.rect = self.image.get_rect()

        self.previous_shot_time = 0

        self.rect.x = x_coord
        self.rect.y = y_coord
        self.health = 5

        self.shootsoundpath1 = os.path.join(
            dirname, "..", "assets", "piu.wav")

        self.shootsoundpath2 = os.path.join(
            dirname, "..", "assets", "pum.wav")

        self.shootsoundpath3 = os.path.join(
            dirname, "..", "assets", "pam.wav")

    def give_coords(self):
        return (self.rect.x, self.rect.y)

    def can_shoot(self, current_time):
        return current_time - self.previous_shot_time >= 1000

    def is_dead(self):
        if self.health <= 0:
            return True
        return False
