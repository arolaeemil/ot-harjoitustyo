import os
import pygame

dirname = os.path.dirname(__file__)

class Blob(pygame.sprite.Sprite):
    def __init__(self, x_coord=0, y_coord=0):
        """enemy projectile
        Args:
            x_coord (int, optional): starting x-coordinate
            y_coord (int, optional): starting y-coordinate
        """
        super().__init__()
        self.previous_move_time = 0

        self.image = pygame.image.load(os.path.join(
            dirname, "..", "assets", "blob.png"))
        self.rect = self.image.get_rect()

        # starting x- and y-coordinates
        self.rect.x = x_coord
        self.rect.y = y_coord

    def should_move(self, current_time):
        return current_time - self.previous_move_time >= 30

    def give_coords(self):
        return (self.rect.x, self.rect.y)
