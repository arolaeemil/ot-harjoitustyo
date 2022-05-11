import os
import unittest
from random import randint
from level import Level
from sprites.basicenemy import Basicenemy
from sprites.boss import Boss
from sprites.shot import Shot
from sprites.blob import Blob


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
        self.level = Level(LEVEL_MAP, CELL_SIZE, 3, 0)
        self.level_medium = Level(LEVEL_MAP, CELL_SIZE, 2, 0)
        self.level_hard = Level(LEVEL_MAP, CELL_SIZE, 1, 0)

    def assert_coordinates_equal(self, sprite, x, y):
        self.assertEqual(sprite.rect.x, x)
        self.assertEqual(sprite.rect.y, y)
    
    def test_difficulties_work(self):
        self.assertEqual(self.level.enemyspeed, 1)
        self.assertEqual(self.level.enemylimit, 5)
        self.assertEqual(self.level.extra_score, 1)
        self.assertEqual(self.level_medium.enemyspeed, 1.5)
        self.assertEqual(self.level_medium.enemylimit, 6)
        self.assertEqual(self.level_medium.extra_score, 2)
        self.assertEqual(self.level_hard.enemylimit, 7)
        self.assertEqual(self.level_hard.enemyspeed, 2)
        self.assertEqual(self.level_hard.extra_score, 3)

    def test_can_move(self):
        ship = self.level.ship
        self.assert_coordinates_equal(ship, 5 * CELL_SIZE, 5 * CELL_SIZE)

        self.level.move_ship(diff_y=-CELL_SIZE)
        self.assert_coordinates_equal(ship, 5 * CELL_SIZE, 4 * CELL_SIZE)

        self.level.move_ship(diff_x=-CELL_SIZE)
        self.assert_coordinates_equal(ship, 4 * CELL_SIZE, 4 * CELL_SIZE)

    def test_cant_move_out(self):
        ship = self.level.ship
        self.assert_coordinates_equal(ship, 5 * CELL_SIZE, 5 * CELL_SIZE)
        for i in range(1, 10000):
            self.level.move_ship(diff_x=-CELL_SIZE)
            self.level.move_ship(diff_y=-CELL_SIZE)
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
        self.assertEqual(len(self.level.enemies), 5)
    
    def test_enemies_spawn_from_portals_and_portals_fade(self):
        current_time = 10000
        for i in range(0,10):
            self.level.spawn_enemies(current_time)
        self.assertEqual(len(self.level.portals), 4)
        current_time = 20000
        self.level.update(current_time)
        self.assertEqual(len(self.level.portals), 0)

    def test_boss_can_spawn(self):
        self.level.bosscounter = 15
        current_time = 10000
        self.level.spawn_boss(current_time)
        self.assertEqual(len(self.level.bosses), 1)

    def test_boss_can_die(self):
        self.level.bosscounter = 15
        current_time = 10000
        self.level.spawn_boss(current_time)
        for boss in self.level.bosses:
            boss.remove_hp(10)
            self.level.shots.add(Shot(25*CELL_SIZE, 10*CELL_SIZE))
            self.assertEqual(boss.is_kill(), True)
        self.level.boss_got_hit(current_time)
        self.assertEqual(len(self.level.bosses), 0)

    def test_update_shots(self):
        test_shot = Shot(100,100)
        current_time = 50
        self.level.shots.add(test_shot)
        self.level.update_shots(current_time)
        test_x, test_y = test_shot.give_coords()
        self.assertEqual(test_y, 100-(10*self.level.gamespeed))
        self.assertEqual(test_x, 100)
        test_shot = Shot(0,0)
        current_time = 50
        self.level.shots.add(test_shot)
        self.level.update_shots(current_time)
        test_x, test_y = test_shot.give_coords()
        self.assertEqual(len(self.level.shots), 1)
    
    def test_update_blobs(self):
        test_blob = Blob(100,100)
        current_time = 50
        self.level.blobs.add(test_blob)
        self.level.update_blobs(current_time)
        test_x, test_y = test_blob.give_coords()
        self.assertEqual(test_y, 100+(2*self.level.gamespeed))
        self.assertEqual(test_x, 100)
        test_blob = Blob(0,0)
        current_time = 50
        self.level.shots.add(test_blob)
        self.level.update_shots(current_time)
        test_x, test_y = test_blob.give_coords()
        self.assertEqual(len(self.level.blobs), 1)

    def test_boss_moves_and_shoots(self):
        test_boss = Boss(400,400)
        boss_x, boss_y = test_boss.give_coords()
        self.level.bosses.add(test_boss)
        current_time = 10000
        self.level.boss_actions(current_time)
        new_boss_x, new_boss_y = test_boss.give_coords()
        is_same_coord = boss_x == new_boss_x
        self.assertEqual(is_same_coord, False)
        self.assertEqual(boss_y, new_boss_y)
        self.assertEqual(len(self.level.blobs), 1)