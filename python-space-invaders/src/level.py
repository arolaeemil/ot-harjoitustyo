from sprites.spaceship import *
from sprites.space import Space
from sprites.shot import *
from sprites.blocker import Blocker
import pygame


class Level:
    def __init__(self, level_map, cell_size):
        self.cell_size = cell_size
        self.ship = None
        self.spaces = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.shots = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()

        self._initialize_sprites(level_map)

    def _initialize_sprites(self, level_map):
            height = len(level_map)
            width = len(level_map[0])

            for y in range(height):
                for x in range(width):
                    cell = level_map[y][x]
                    normalized_x = x * self.cell_size
                    normalized_y = y * self.cell_size

                    if cell == 1:
                        self.ship = Spaceship(normalized_x, normalized_y)
                        #self.spaces.add(Space(normalized_x, normalized_y))
                    elif cell == 0:
                        pass
                        #self.spaces.add(Space(normalized_x, normalized_y))
                    elif cell == 2:
                        self.walls.add(Blocker(normalized_x, normalized_y))

            #elf.all_sprites.add(self.spaces, self.walls, self.ship, self.shots)        
            self.all_sprites.add(self.walls, self.ship, self.shots)

    def ship_can_move(self, dx=0, dy=0):
        # move ship to new position
        self.ship.rect.move_ip(dx, dy)
        # check if robot hits boundary
        colliding_walls = pygame.sprite.spritecollide(self.ship, self.walls, False)
        can_move = not colliding_walls
        # move ship back to original position
        self.ship.rect.move_ip(-dx, -dy)
        return can_move

    def update(self, current_time):
        for shot in self.shots:
            if shot.should_move(current_time):
                self.move_shot(shot)
                shot.previous_move_time = current_time

    def move_ship(self, dx=0, dy=0):
        if not self.ship_can_move(dx, dy):
            return
        self.ship.rect.move_ip(dx, dy)

    def move_shot(self,shot):
        shot.rect.move_ip(0, -10)

    def shoot(self, ship, current_time):
        if not ship.can_shoot(current_time):
            return False
        ship.previous_shot_time = current_time
        coords = ship.give_coords()
        new_shot = Shot(coords[0], coords[1])
        self.shots.add(new_shot)
        self.all_sprites.add(self.shots)
        return True