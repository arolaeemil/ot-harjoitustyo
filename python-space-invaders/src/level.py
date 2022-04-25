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


class Level:
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
        self.blobs = pygame.sprite.Group()
        self.gamespeed = 1
        self.score = 0
        #chance the value of the sound_on to 1 if you want to enjoy simple sounds. 
        #The automated tests do not work with sounds at the moment.
        self.sound_on = 1

        self._initialize_sprites(level_map)

    def _initialize_sprites(self, level_map):
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

        #elf.all_sprites.add(self.spaces, self.walls, self.ship, self.shots)
        self.all_sprites.add(self.walls, self.explosions,
                             self.enemies, self.ship, self.shots, self.portals)

    def ship_can_move(self, diff_x=0, diff_y=0):
        # move ship to new position
        self.ship.rect.move_ip(diff_x, diff_y)
        # check if robot hits boundary
        colliding_walls = pygame.sprite.spritecollide(
            self.ship, self.walls, False)
        can_move = not colliding_walls
        # move ship back to original position
        self.ship.rect.move_ip(-diff_x, -diff_y)
        return can_move

    def update(self, current_time):
        # ship alive things
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
        # enemies
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

    def move_ship(self, diff_x=0, diff_y=0):
        if not self.ship_can_move(diff_x, diff_y):
            return
        self.ship.rect.move_ip(diff_x, diff_y)

    def move_shot(self, shot):
        shot.rect.move_ip(0, -10*self.gamespeed)

    def shoot(self, ship, current_time):
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
        is_dead = self.ship.is_dead()
        if is_dead is True:
            # print("GAME_OVER")
            return True
        return False

    #score and hp

    def draw_hp_bar(self, display):
        location = (self.ship.rect.x, self.ship.rect.y, 0, 0)
        pygame.draw.rect(display, (255, 0, 0),
                         (location[0], location[1] - 20, 50, 15))
        pygame.draw.rect(display, (0, 128, 0),
                         (location[0], location[1] - 20, 50 - (10 * (5 - self.ship.health)), 15))

    def draw_score(self, display):
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

    # enemy actions

    def move_enemy(self, enemy, diff_x=0, diff_y=0):
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
        #colliding_shots = pygame.sprite.groupcollide(self.enemies, self.shots, True, True)
        #colliding_enemies = pygame.sprite.groupcollide(self.shots, self.enemies, True, True)
        # remove enemy, add explosion on hit
        # print(colliding_shots)
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
            # remove hit enemy
            for enemies in colliding_enemies:
                for enemy in enemies:
                    coords.append(enemy.give_coords())
                    #pygame.sprite.Sprite.remove(e, self.all_sprites, self.enemies)
                    pygame.sprite.Sprite.kill(enemy)
                    if self.sound_on == 1:
                        sound = pygame.mixer.Sound(self.ship.shootsoundpath3)
                        pygame.mixer.Sound.play(sound)
                    self.score = self.score + 1
                    # self.enemies.remove(e)
            # self.all_sprites.remove(self.enemy)
            #self.enemy = None
            # remove hit shot
            for shots in colliding_shots:
                for shot in shots:
                    # self.all_sprites.remove(s)
                    #pygame.sprite.Sprite.remove(s, self.all_sprites, self.shots)
                    pygame.sprite.Sprite.kill(shot)
                    # self.shots.remove(s)
            # print(coords)
            # add explosion effect
            for coord in coords:
                new_exp = Explosion(coord[0], coord[1], current_time)
                self.explosions.add(new_exp)
                self.all_sprites.add(self.explosions)
            # print(self.explosions)

    def move_blob(self, blob):
        blob.rect.move_ip(0, self.gamespeed*2)

    def enemy_blob(self, enemy, current_time):
        if not enemy.can_shoot(current_time):
            return False
        enemy.previous_shot_time = current_time
        coords = enemy.give_coords()
        new_blob = Blob(coords[0], coords[1])
        self.blobs.add(new_blob)
        self.all_sprites.add(self.blobs)
        return True

    # enemy spawning
    def spawn_enemies(self, current_time):
        choose_type = choice([1, 2])
        x_coord = randint(10, 55)
        y_coord = randint(10, 25)
        normalized_x = x_coord * self.cell_size
        normalized_y = y_coord * self.cell_size
        # print(len(self.enemies))
        if len(self.enemies) < 10:
            self.enemies.add(Basicenemy(
                normalized_x, normalized_y, choose_type))
            self.portals.add(
                Explosion(normalized_x, normalized_y, current_time, 2))
            self.all_sprites.add(self.portals, self.enemies)

    # top score

    def save_score(self):
        script_path = os.path.dirname(os.path.abspath(__file__))
        rel_path = "record.txt"
        abs_file_path = os.path.join(script_path, rel_path)
        #print(abs_file_path)
        with open(abs_file_path, "a+", encoding="utf-8") as file:
            file.write(str(self.score))
            file.write("\n")
