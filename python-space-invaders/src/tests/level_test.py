import unittest
from level import Level

# test map
n = 100
LEVEL_MAP = []
for i in range(0, n):
    LEVEL_MAP.append([])
    for j in range(0, n):
        if j == 0 or j == (n-1) or i == 0 or i == (n-1):
            LEVEL_MAP[i].append(2)
        else:
            LEVEL_MAP[i].append(0)
LEVEL_MAP[5][5] = 1
CELL_SIZE = 10


class TestLevel(unittest.TestCase):
    def setUp(self):
        self.level = Level(LEVEL_MAP, CELL_SIZE)
        # pass

    def assert_coordinates_equal(self, sprite, x, y):
        self.assertEqual(sprite.rect.x, x)
        self.assertEqual(sprite.rect.y, y)
        # pass

    def test_can_move(self):
        ship = self.level.ship
        self.assert_coordinates_equal(ship, 5 * CELL_SIZE, 5 * CELL_SIZE)

        self.level.move_ship(dy=-CELL_SIZE)
        self.assert_coordinates_equal(ship, 5 * CELL_SIZE, 4 * CELL_SIZE)

        self.level.move_ship(dx=-CELL_SIZE)
        self.assert_coordinates_equal(ship, 4 * CELL_SIZE, 4 * CELL_SIZE)
        # pass

    def test_cant_move_out(self):
        ship = self.level.ship
        self.assert_coordinates_equal(ship, 5 * CELL_SIZE, 5 * CELL_SIZE)
        for i in range(1, 10000):
            self.level.move_ship(dx=-CELL_SIZE)
            self.level.move_ship(dy=-CELL_SIZE)
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
