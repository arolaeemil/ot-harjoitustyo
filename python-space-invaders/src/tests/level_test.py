import os
import unittest
#import pygame
from random import randint
from level import Level
from sprites.basicenemy import Basicenemy
from sprites.shot import Shot
from sprites.blob import Blob

# test map
#n = 100
#LEVEL_MAP = []
# for i in range(0, n):
# LEVEL_MAP.append([])
# for j in range(0, n):
# if j == 0 or j == (n-1) or i == 0 or i == (n-1):
# LEVEL_MAP[i].append(2)
# else:
# LEVEL_MAP[i].append(0)
#LEVEL_MAP[5][5] = 1

CELL_SIZE = 10

N = 70

LEVEL_MAP = []
for i in range(0, N):
    LEVEL_MAP.append([])
    for j in range(0, N):
        if j == 0 or j == (N-1) or i == 0 or i == (N-1):
            LEVEL_MAP[i].append(2)
        else:
            LEVEL_MAP[i].append(0)


LEVEL_MAP[5][5] = 1

LEVEL_MAP[10][10] = 3

# test map creation ends


class TestLevel(unittest.TestCase):
    def setUp(self):
        self.level = Level(LEVEL_MAP, CELL_SIZE)
        #pygame.mixer.init()
        # pass

    def assert_coordinates_equal(self, sprite, x, y):
        self.assertEqual(sprite.rect.x, x)
        self.assertEqual(sprite.rect.y, y)
        # pass

    def test_can_move(self):
        ship = self.level.ship
        self.assert_coordinates_equal(ship, 5 * CELL_SIZE, 5 * CELL_SIZE)

        self.level.move_ship(diff_y=-CELL_SIZE)
        self.assert_coordinates_equal(ship, 5 * CELL_SIZE, 4 * CELL_SIZE)

        self.level.move_ship(diff_x=-CELL_SIZE)
        self.assert_coordinates_equal(ship, 4 * CELL_SIZE, 4 * CELL_SIZE)
        # pass

    def test_cant_move_out(self):
        ship = self.level.ship
        self.assert_coordinates_equal(ship, 5 * CELL_SIZE, 5 * CELL_SIZE)
        for i in range(1, 10000):
            self.level.move_ship(diff_x=-CELL_SIZE)
            self.level.move_ship(diff_y=-CELL_SIZE)
        # border is at 2 cellsize at the moment
        self.assert_coordinates_equal(ship, 2 * CELL_SIZE, 2 * CELL_SIZE)

    def test_can_shoot_cooldown_timer_works(self):
        ship = self.level.ship
        current_time = 10000
        self.level.shoot(ship, current_time)
        self.assertEqual(len(self.level.shots), 1)
        current_time = 11000
        self.level.shoot(ship, current_time)
        current_time = 11000
        self.level.shoot(ship, current_time)
        self.assertEqual(len(self.level.shots), 2)
        current_time = 12000
        self.level.shoot(ship, current_time)
        current_time = 13000
        self.level.shoot(ship, current_time)
        self.assertEqual(len(self.level.shots), 4)

    def test_enemies_spawn(self):
        enemy_list = self.level.enemies
        self.assertEqual(len(enemy_list), 1)

    def test_enemies_shoot(self):
        blob_list = self.level.blobs
        enemy_list = self.level.enemies
        current_time = 1000000
        for enemy in enemy_list:
            self.level.enemy_blob(enemy, current_time)
        self.assertEqual(len(blob_list), 1)

    def test_player_can_die(self):
        self.level.ship.health = self.level.ship.health - 10
        self.assertEqual(self.level.ship_is_kill(), True)

    def test_score_works(self):
        self.level.score = self.level.score + 10
        self.assertEqual(self.level.score, 10)

    def test_enemy_can_die_and_explodes(self):
        current_time = 10000
        #self.level.shoot(self.level.ship, current_time)
        self.level.shots.add(Shot(10*CELL_SIZE, 10*CELL_SIZE))
        self.level.enemy_got_hit(current_time)
        self.assertEqual(len(self.level.enemies), 0)
        self.assertEqual(len(self.level.explosions), 1)

    def test_player_can_get_hit(self):
        current_time = 10000
        self.level.blobs.add(Blob(5*CELL_SIZE, 5*CELL_SIZE))
        self.level.ship_got_hit(current_time)
        self.assertEqual(self.level.ship.health, 4)
        self.assertEqual(len(self.level.blobs), 0)

    def test_enemies_can_spawn(self):
        current_time = 10000
        for i in range(0,20):
            self.level.spawn_enemies(current_time)
        self.assertEqual(len(self.level.enemies), 10)
    
    def test_enemies_spawn_from_portals_and_portals_fade(self):
        current_time = 10000
        for i in range(0,10):
            self.level.spawn_enemies(current_time)
        self.assertEqual(len(self.level.portals), 9)
        current_time = 20000
        self.level.update(current_time)
        self.assertEqual(len(self.level.portals), 0)

    def test_score_is_saved(self):
        self.level.score = 20
        self.level.save_score()
        rel_path = os.path.join("src", "record.txt")
        with open(rel_path, "r") as file:
            for line in file:
                pass
            last_line = line
        self.assertEqual(int(last_line), 20)

