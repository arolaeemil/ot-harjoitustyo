import os
import pygame

# path to get the file
dirname = os.path.dirname(__file__)

# sprite class is inherited


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x_coord=0, y_coord=0, current_time=0, what_type=1):
        """purely graphical effects with a fade timer, can give several types for different pictures
        Args:
            x_coord (int, optional): x_coordinate
            y_coord (int, optional): y_coordinate
            current_time (int, optional): birth time is given
            what_type (int, optional): chosen type
        """
        super().__init__()
        self.what_type = what_type

        # getting the image for the ship
        if self.what_type == 1:
            self.image = pygame.image.load(
                os.path.join(dirname, "..", "assets", "explosion.png"))
        if self.what_type == 2:
            self.image = pygame.image.load(
                os.path.join(dirname, "..", "assets", "portal.png"))
        if self.what_type == 3:
            self.image = pygame.image.load(
                os.path.join(dirname, "..", "assets", "blob_exp.png"))
        if self.what_type == 4:
            self.image = pygame.image.load(
            os.path.join(dirname, "..", "assets", "boss_death.png"))
        if self.what_type == 5:
            self.image = pygame.image.load(
                os.path.join(dirname, "..", "assets", "boss_portal.png"))
        # rectacular shape (50x50)
        self.rect = self.image.get_rect()
        # for fire cooldown
        # starting x- and y-coordinates
        self.rect.x = x_coord
        self.rect.y = y_coord
        self.birth_time = current_time

    def give_coords(self):
        return (self.rect.x, self.rect.y)

    def can_fade(self, current_time):
        return current_time - self.birth_time >= 1500
