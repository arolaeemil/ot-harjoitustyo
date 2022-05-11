import os
import pygame

dirname = os.path.dirname(__file__)

class Shot(pygame.sprite.Sprite):
    def __init__(self, x_coord=0, y_coord=0):
        """player projectile
        Args:
            x_coord (int, optional): starting x-coordinate
            y_coord (int, optional): starting y-coordinate
        """
        super().__init__()
        self.previous_move_time = 0

        self.image = pygame.image.load(os.path.join(
            dirname, "..", "assets", "missile.png"))
        self.rect = self.image.get_rect()

        self.rect.x = x_coord
        self.rect.y = y_coord

    def should_move(self, current_time):
        """Tells if shot should move
        Returns:
            True: if should move
            False: if should not move yet
        """
        return current_time - self.previous_move_time >= 15

    def give_coords(self):
        """Gives x- and y-coordinates
        Returns:
            x-coordinate, y-coordinate
        """
        return (self.rect.x, self.rect.y)
