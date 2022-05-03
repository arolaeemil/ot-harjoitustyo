import os
from random import randint, choice
import pygame
from sprites.spaceship import Spaceship
#from sprites.space import Space
from sprites.shot import Shot
from sprites.blob import Blob
from sprites.blocker import Blocker
from sprites.basicenemy import Basicenemy
from sprites.explosion import Explosion
from sprites.boss import Boss

class Level:
    """This class is responsible for the most of the basic
    functionality considering the behaviour of different objects
    """
    def __init__(self, level_map, cell_size):
        self.cell_size = cell_size
        self.ship = None
        self.portals = pygame.sprite.Group()
        self.spaces = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.shots = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.enemy = None
        self.bosses = pygame.sprite.Group()
        self.blobs = pygame.sprite.Group()
        self.gamespeed = 1
        self.score = 0
        self.bosscounter = 0
        #chance the value of the sound_on to 1 if you want to enjoy simple sounds.
        #The automated tests do not work with sounds at the moment.
        self.sound_on = 0

        self._initialize_sprites(level_map)

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
                    #self.spaces.add(Space(normalized_x, normalized_y))
                elif cell == 0:
                    pass
                    #self.spaces.add(Space(normalized_x, normalized_y))
                elif cell == 2:
                    self.walls.add(Blocker(normalized_x, normalized_y))
                elif cell == 3:
                    self.enemies.add(Basicenemy(normalized_x, normalized_y))
                    #self.enemy = Basicenemy(normalized_x, normalized_y)

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
        # shots
        for shot in self.shots:
            if shot.should_move(current_time):
                self.move_shot(shot)
                shot.previous_move_time = current_time
                if pygame.sprite.spritecollide(shot, self.walls, False):
                    self.all_sprites.remove(shot)
                    self.shots.remove(shot)
        for blob in self.blobs:
            if blob.should_move(current_time):
                self.move_blob(blob)
                blob.previous_move_time = current_time
                if pygame.sprite.spritecollide(blob, self.walls, False):
                    self.all_sprites.remove(blob)
                    self.shots.remove(blob)
        # enemies and bosses
        if len(self.enemies) != 0:
            self.enemy_got_hit(current_time)
        if len(self.enemies) != 0:
            # print(self.enemies)
            # print(len(self.enemies))
            for enemy in self.enemies:
                self.enemy_blob(enemy, current_time)
                if enemy.should_move(current_time):
                    self.move_enemy(enemy)
                    enemy.previous_move_time = current_time
        if len(self.bosses) != 0:
            self.boss_got_hit(current_time)
            for boss in self.bosses:
                self.enemy_blob(boss, current_time)
                if boss.should_move(current_time):
                    self.move_enemy(boss)
                    boss.previous_move_time = current_time
        # effects
        if len(self.explosions) != 0:
            for exp in self.explosions:
                if exp.can_fade(current_time) is True:
                    pygame.sprite.Sprite.kill(exp)
        if len(self.portals) != 0:
            for port in self.portals:
                if port.can_fade(current_time) is True:
                    pygame.sprite.Sprite.kill(port)
                    # self.explosions.remove(exp)
                    # self.all_sprites.remove(exp)

        self.spawn_enemies(current_time)
        self.spawn_boss(current_time)

    def move_ship(self, diff_x=0, diff_y=0):
        if not self.ship_can_move(diff_x, diff_y):
            return
        self.ship.rect.move_ip(diff_x, diff_y)

    def move_shot(self, shot):
        shot.rect.move_ip(0, -10*self.gamespeed)

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
            new_exp = Explosion(coord[0], coord[1], current_time, 3)
            self.explosions.add(new_exp)
            self.all_sprites.add(self.explosions)
            self.ship.health = self.ship.health - 1
            #print("U GOT HIT")
        is_collide = pygame.sprite.spritecollide(self.ship, self.enemies, True)
        if is_collide:
            if self.sound_on == 1:
                sound = pygame.mixer.Sound(self.ship.shootsoundpath2)
                pygame.mixer.Sound.play(sound)
            self.ship.health = self.ship.health - 1
            #print("U GOT HIT")
            coord = self.ship.give_coords()
            new_exp = Explosion(coord[0], coord[1], current_time)
            self.explosions.add(new_exp)
            self.all_sprites.add(self.explosions)
        # if self.ship.is_dead():
            # self.ship_is_kill()

    def ship_is_kill(self):
        """checks the status of the ship
        Returns:
            True if ship is dead
            False if ship is alive
        """
        is_dead = self.ship.is_dead()
        if is_dead is True:
            # print("GAME_OVER")
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
        diff_x = 2*self.gamespeed
        diff_y = 2*self.gamespeed
        # for enemy in self.enemies:
        #print([enemy.movespeed_x, enemy.movespeed_y])
        if not self.enemy_can_move_x(enemy, enemy.movespeed_x*diff_x):
            enemy.movespeed_x = enemy.movespeed_x*(-1)
            # return
        if not self.enemy_can_move_y(enemy, enemy.movespeed_y*diff_y):
            enemy.movespeed_y = enemy.movespeed_y*(-1)
            # return
            # print(enemy.what_type)
        enemy.rect.move_ip(enemy.movespeed_x*diff_x, enemy.movespeed_y*diff_y)
        #enemy.rect.move_ip(1, 1)

    def enemy_can_move_x(self, enemy, diff_x):
        """checks if enemy can move in x-direction without colliding to a wall
        Returns:
            True if enemy can move
            False if enemy cant move
        """
        # move enemy to new position
        enemy.rect.move_ip(diff_x, 0)
        # check if enemy hits boundary
        colliding_walls = pygame.sprite.spritecollide(
            enemy, self.walls, False)
        can_move = not colliding_walls
        # move enemy back to original position
        enemy.rect.move_ip(-diff_x, 0)
        return can_move

    def enemy_can_move_y(self, enemy, diff_y):
        """checks if enemy can move in x-direction without colliding to a wall
        Returns:
            True if enemy can move
            False if enemy cant move
        """
        # move enemy to new position
        enemy.rect.move_ip(0, diff_y)
        # check if enemy hits boundary
        colliding_walls = pygame.sprite.spritecollide(
            enemy, self.walls, False)
        can_move = not colliding_walls
        # move enemy back to original position
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
                    self.score = self.score + 1
                    self.bosscounter = self.bosscounter + 1

            for shots in colliding_shots:
                for shot in shots:
                    pygame.sprite.Sprite.kill(shot)
            # add explosion effect
            for coord in coords:
                new_exp = Explosion(coord[0], coord[1], current_time)
                self.explosions.add(new_exp)
                self.all_sprites.add(self.explosions)

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
                        new_exp = Explosion(new_coord[0], new_coord[1], current_time, 4)
                        self.explosions.add(new_exp)
                        self.all_sprites.add(self.explosions)
                        pygame.sprite.Sprite.kill(boss)
                    if self.sound_on == 1:
                        sound = pygame.mixer.Sound(self.ship.shootsoundpath3)
                        pygame.mixer.Sound.play(sound)
            for shots in colliding_shots:
                for shot in shots:
                    pygame.sprite.Sprite.kill(shot)
            for coord in coords:
                new_exp = Explosion(coord[0], coord[1], current_time)
                self.explosions.add(new_exp)
                self.all_sprites.add(self.explosions)


    def move_blob(self, blob):
        """moves an enemy projectile
        """
        blob.rect.move_ip(0, self.gamespeed*2)

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
        # print(len(self.enemies))
        if len(self.enemies) < 5 and len(self.bosses) == 0:
            self.enemies.add(Basicenemy(
                normalized_x, normalized_y, choose_type))
            self.portals.add(Explosion(normalized_x, normalized_y, current_time, 2))
            self.all_sprites.add(self.portals, self.enemies)

    def spawn_boss(self, current_time):
        if self.bosscounter > 10 and len(self.bosses) == 0:
            start_x = 25*self.cell_size
            start_y = 10*self.cell_size
            self.bosscounter = 0
            self.bosses.add(Boss(start_x, start_y, 1))
            new_portal = Explosion(start_x, start_y, current_time, 5)
            self.portals.add(new_portal)
            self.all_sprites.add(self.portals, self.bosses)

    def save_score(self):
        """saves score to txt-file.
        """
        script_path = os.path.dirname(os.path.abspath(__file__))
        rel_path = "record.txt"
        abs_file_path = os.path.join(script_path, rel_path)
        #print(abs_file_path)
        with open(abs_file_path, "a+", encoding="utf-8") as file:
            file.write(str(self.score))
            file.write("\n")
