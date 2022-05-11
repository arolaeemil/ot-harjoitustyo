from random import randint, choice
import pygame
from sprites.spaceship import Spaceship
from sprites.shot import Shot
from sprites.blob import Blob
from sprites.blocker import Blocker
from sprites.basicenemy import Basicenemy
from sprites.explosion import Explosion
from sprites.boss import Boss
from high_scorehandler import make_record_handler

class Level:
    """This class is responsible for the most of the basic
    functionality considering the behaviour of different objects
    """
    def __init__(self, level_map, cell_size, game_difficulty, sound_on_off):
        self.cell_size = cell_size
        self.ship = None
        self.score = 0
        self.bosscounter = 0
        self.gamespeed = 1
        self._determine_difficulty(game_difficulty)
        self._create_spritegroups()
        self._initialize_sprites(level_map)
        self.record_handler = make_record_handler()
        self.sound_on = sound_on_off

    def _create_spritegroups(self):
        """creates the groups of sprites.
        """
        self.portals = pygame.sprite.Group()
        self.spaces = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.shots = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bosses = pygame.sprite.Group()
        self.blobs = pygame.sprite.Group()

    def _determine_difficulty(self, game_difficulty):
        """Determines game difficulty based on the gotten value. Difficulty consists
        from enemy speed, enemy limit and also increases score gained
        """
        if game_difficulty == 1:
            self.enemyspeed = 2
            self.enemylimit = 7
            self.extra_score = 3
        elif game_difficulty == 2:
            self.enemyspeed = 1.5
            self.enemylimit = 6
            self.extra_score = 2
        elif game_difficulty == 3:
            self.enemyspeed = 1
            self.enemylimit = 5
            self.extra_score = 1

    def _initialize_sprites(self, level_map):
        """initialises the sprite objects based on level map
        Args:
           level_map, contains starting positions of objects
        """
        height = len(level_map)
        width = len(level_map[0])

        for y_coord in range(height):
            for x_coord in range(width):
                cell = level_map[y_coord][x_coord]
                normalized_x = x_coord * self.cell_size
                normalized_y = y_coord * self.cell_size

                if cell == 1:
                    self.ship = Spaceship(normalized_x, normalized_y)
                elif cell == 0:
                    pass
                elif cell == 2:
                    self.walls.add(Blocker(normalized_x, normalized_y))
                elif cell == 3:
                    self.enemies.add(Basicenemy(normalized_x, normalized_y))

        self.all_sprites.add(self.walls, self.explosions,
                             self.enemies, self.ship, self.shots, self.portals, self.bosses)

    def ship_can_move(self, diff_x=0, diff_y=0):
        """test if the ship can move without hitting a boundary
        Args:
            diff_x (int, optional): difference in x-coordinate. Defaults to 0.
            diff_y (int, optional): difference in y-coordinate. Defaults to 0.
        Returns:
            True if ship can make the movement
        """
        self.ship.rect.move_ip(diff_x, diff_y)
        colliding_walls = pygame.sprite.spritecollide(
            self.ship, self.walls, False)
        can_move = not colliding_walls

        self.ship.rect.move_ip(-diff_x, -diff_y)
        return can_move

    def update(self, current_time):
        """this method updates the situation of the sprites such as locations and graphical effects
        """
        self.ship_got_hit(current_time)
        self.update_shots(current_time)
        self.update_blobs(current_time)
        #enemies and bosses
        if len(self.enemies) != 0:
            self.enemy_got_hit(current_time)
        if len(self.enemies) != 0:
            self.enemy_actions(current_time)
        if len(self.bosses) != 0:
            self.boss_got_hit(current_time)
            self.boss_actions(current_time)
        #graphical effects
        self.fade_graphical_effects(current_time)
        #enemy spawns
        self.spawn_enemies(current_time)
        self.spawn_boss(current_time)

    def move_ship(self, diff_x=0, diff_y=0):
        """moves the player ship in x and y directions.
        """
        if not self.ship_can_move(diff_x, diff_y):
            return
        self.ship.rect.move_ip(diff_x, diff_y)

    def move_shot(self, shot):
        """moves a shot object.
        """
        shot.rect.move_ip(0, -10*self.gamespeed)

    def update_shots(self, current_time):
        """moves shots and checks collisions to walls.
        """
        for shot in self.shots:
            if shot.should_move(current_time):
                self.move_shot(shot)
                shot.previous_move_time = current_time
                if pygame.sprite.spritecollide(shot, self.walls, False):
                    self.all_sprites.remove(shot)
                    self.shots.remove(shot)

    def shoot(self, ship, current_time):
        """shoots based on a cooldown and plays a sound if the sound effects are enabled

        Returns:
            True if ship can shoot, also creates a new shot to the game
            False if ship can't shoot
        """
        if not ship.can_shoot(current_time):
            return False
        if self.sound_on == 1:
            sound = pygame.mixer.Sound(self.ship.shootsoundpath1)
            pygame.mixer.Sound.play(sound)
        ship.previous_shot_time = current_time
        coords = ship.give_coords()
        new_shot = Shot(coords[0], coords[1])
        self.shots.add(new_shot)
        self.all_sprites.add(self.shots)
        return True

    def ship_got_hit(self, current_time):
        """lowers ship health if it gets hit by a damaging other sprite. Also adds graphical effect.
        """
        is_hit = pygame.sprite.spritecollide(self.ship, self.blobs, True)
        if is_hit:
            if self.sound_on == 1:
                sound = pygame.mixer.Sound(self.ship.shootsoundpath2)
                pygame.mixer.Sound.play(sound)
            coord = self.ship.give_coords()
            self.make_one_explosion(coord,current_time,1)
            self.ship.health = self.ship.health - 1
        is_collide = pygame.sprite.spritecollide(self.ship, self.enemies, True)
        if is_collide:
            if self.sound_on == 1:
                sound = pygame.mixer.Sound(self.ship.shootsoundpath2)
                pygame.mixer.Sound.play(sound)
            self.ship.health = self.ship.health - 1
            coord = self.ship.give_coords()
            self.make_one_explosion(coord, current_time, 1)

    def ship_is_kill(self):
        """checks the status of the ship
        Returns:
            True if ship is dead
            False if ship is alive
        """
        is_dead = self.ship.is_dead()
        if is_dead is True:
            return True
        return False

    def draw_hp_bar(self, display):
        """draws the hp bar based on ship health
        """
        location = (self.ship.rect.x, self.ship.rect.y, 0, 0)
        pygame.draw.rect(display, (255, 0, 0),
                         (location[0], location[1] - 20, 50, 15))
        pygame.draw.rect(display, (0, 128, 0),
                         (location[0], location[1] - 20, 50 - (10 * (5 - self.ship.health)), 15))

    def draw_score(self, display):
        """draws the scorebox
        """
        location = pygame.display.get_window_size()
        font = pygame.font.SysFont("Arial", 36)
        x_coord = location[0]/20
        y_coord = location[1]/20
        text = font.render(str(self.score), True, (255, 0, 0))
        wid = 100
        height = 50
        pygame.draw.rect(display, (0, 0, 255),
                         (x_coord-10, y_coord-10, wid+20, height+20))
        pygame.draw.rect(display, (0, 0, 0), (x_coord, y_coord, wid, height))
        display.blit(text, (x_coord+(wid/10), y_coord))

    def move_enemy(self, enemy, diff_x=0, diff_y=0):
        """moves an enemy
        """
        diff_x = 2*self.enemyspeed
        diff_y = 2*self.enemyspeed
        if not self.enemy_can_move_x(enemy, enemy.movespeed_x*diff_x):
            enemy.movespeed_x = enemy.movespeed_x*(-1)
        if not self.enemy_can_move_y(enemy, enemy.movespeed_y*diff_y):
            enemy.movespeed_y = enemy.movespeed_y*(-1)
        enemy.rect.move_ip(enemy.movespeed_x*diff_x, enemy.movespeed_y*diff_y)

    def enemy_actions(self, current_time):
        """makes enemies move and shoot
        """
        for enemy in self.enemies:
            self.enemy_blob(enemy, current_time)
            if enemy.should_move(current_time):
                self.move_enemy(enemy)
                enemy.previous_move_time = current_time

    def enemy_can_move_x(self, enemy, diff_x):
        """checks if enemy can move in x-direction without colliding to a wall
        Returns:
            True if enemy can move
            False if enemy cant move
        """
        enemy.rect.move_ip(diff_x, 0)
        colliding_walls = pygame.sprite.spritecollide(
            enemy, self.walls, False)
        can_move = not colliding_walls
        enemy.rect.move_ip(-diff_x, 0)
        return can_move

    def enemy_can_move_y(self, enemy, diff_y):
        """checks if enemy can move in x-direction without colliding to a wall
        Returns:
            True if enemy can move
            False if enemy cant move
        """
        enemy.rect.move_ip(0, diff_y)
        colliding_walls = pygame.sprite.spritecollide(
            enemy, self.walls, False)
        can_move = not colliding_walls
        enemy.rect.move_ip(0, -diff_y)
        return can_move

    def enemy_got_hit(self, current_time):
        """removes enemies which get hit by a projectile.
        Also removes the projectile and adds a graphical effect.
        """
        colliding_shots = []
        colliding_enemies = []
        for enemy in self.enemies:
            apu = pygame.sprite.spritecollide(enemy, self.shots, False, False)
            colliding_enemies.append(apu)
        for shot in self.shots:
            apu = pygame.sprite.spritecollide(shot, self.enemies, False, False)
            colliding_shots.append(apu)
        coords = []
        if colliding_shots:
            for enemies in colliding_enemies:
                for enemy in enemies:
                    coords.append(enemy.give_coords())
                    pygame.sprite.Sprite.kill(enemy)
                    if self.sound_on == 1:
                        sound = pygame.mixer.Sound(self.ship.shootsoundpath3)
                        pygame.mixer.Sound.play(sound)
                    self.score = self.score + self.extra_score*1
                    self.bosscounter = self.bosscounter + 1

            for shots in colliding_shots:
                for shot in shots:
                    pygame.sprite.Sprite.kill(shot)
            self.make_small_explosions(coords,current_time, 1)

    def boss_got_hit(self, current_time):
        """removes projectiles which hit boss.
        Also removes hp from boss and adds a graphical effect.
        """
        colliding_shots = []
        colliding_bosses = []
        coords = []
        for shot in self.shots:
            apu = pygame.sprite.spritecollide(shot, self.bosses, False, False)
            colliding_bosses.append(apu)
        for boss in self.bosses:
            apu = pygame.sprite.spritecollide(boss, self.shots, False, False)
            colliding_shots.append(apu)
        if colliding_shots:
            for bosses in colliding_bosses:
                for boss in bosses:
                    boss.remove_hp(1)
                    coords.append(boss.give_coords())
                    if boss.is_kill() is True:
                        new_coord = boss.give_coords()
                        self.make_one_explosion(new_coord, current_time, 4)
                        self.score = self.score + self.extra_score*5
                        pygame.sprite.Sprite.kill(boss)
                    if self.sound_on == 1:
                        sound = pygame.mixer.Sound(self.ship.shootsoundpath3)
                        pygame.mixer.Sound.play(sound)
            for shots in colliding_shots:
                for shot in shots:
                    pygame.sprite.Sprite.kill(shot)
            self.make_small_explosions(coords,current_time, 1)

    def make_small_explosions(self, coords, current_time, effect_type):
        """makes small explosions based on coordinate list.
        """
        for coord in coords:
            new_exp = Explosion(coord[0], coord[1], current_time, effect_type)
            self.explosions.add(new_exp)
            self.all_sprites.add(self.explosions)

    def make_one_explosion(self, coord, current_time, effect_type):
        """makes small explosion based on single coordinate
        """
        new_exp = Explosion(coord[0], coord[1], current_time, effect_type)
        if effect_type in [1,3,4]:
            self.explosions.add(new_exp)
            self.all_sprites.add(self.explosions)
        if effect_type in [2,5]:
            self.portals.add(new_exp)
            self.all_sprites.add(self.portals)

    def boss_actions(self, current_time):
        """makes boss move and shoot
        """
        for boss in self.bosses:
            self.enemy_blob(boss, current_time)
            if boss.should_move(current_time):
                self.move_enemy(boss)
                boss.previous_move_time = current_time


    def move_blob(self, blob):
        """moves an enemy projectile
        """
        blob.rect.move_ip(0, self.gamespeed*2)

    def update_blobs(self, current_time):
        """moves blobs and checks for collisions to walls.
        """
        for blob in self.blobs:
            if blob.should_move(current_time):
                self.move_blob(blob)
                blob.previous_move_time = current_time
                if pygame.sprite.spritecollide(blob, self.walls, False):
                    self.all_sprites.remove(blob)
                    self.shots.remove(blob)

    def enemy_blob(self, enemy, current_time):
        """makes an enemy shoot a projectile if it is not on a cooldown
        Args:
            enemy: an enemy sprite
            current_time: game time
        Returns:
            True if enemy can shoot
            False if enemy cant shoot yet
        """
        if not enemy.can_shoot(current_time):
            return False
        enemy.previous_shot_time = current_time
        coords = enemy.give_coords()
        new_blob = Blob(coords[0], coords[1])
        self.blobs.add(new_blob)
        self.all_sprites.add(self.blobs)
        return True

    def spawn_enemies(self, current_time):
        """spawn new enemies if there is not enough of them.
        Also makes a graphical effect on enemy spawn
        """
        choose_type = choice([1, 2])
        x_coord = randint(10, 55)
        y_coord = randint(10, 25)
        normalized_x = x_coord * self.cell_size
        normalized_y = y_coord * self.cell_size
        if len(self.enemies) < self.enemylimit and len(self.bosses) == 0:
            self.make_one_explosion((normalized_x, normalized_y), current_time, 2)
            self.enemies.add(Basicenemy(
                normalized_x, normalized_y, choose_type))
            self.all_sprites.add(self.enemies)

    def spawn_boss(self, current_time):
        """Spawns a boss enemy if requirements are met.
        """
        if self.bosscounter > 10 and len(self.bosses) == 0:
            start_x = 25*self.cell_size
            start_y = 10*self.cell_size
            self.bosscounter = 0
            self.bosses.add(Boss(start_x, start_y, 1))
            self.make_one_explosion((start_x, start_y), current_time, 5)
            self.all_sprites.add(self.bosses)

    def fade_graphical_effects(self, current_time):
        """removes too old graphical effects
        """
        if len(self.explosions) != 0:
            for exp in self.explosions:
                if exp.can_fade(current_time) is True:
                    pygame.sprite.Sprite.kill(exp)
        if len(self.portals) != 0:
            for port in self.portals:
                if port.can_fade(current_time) is True:
                    pygame.sprite.Sprite.kill(port)

    def save_scoredb(self):
        """saves score to records.db.
        """
        self.record_handler.create_new_score(self.score)
