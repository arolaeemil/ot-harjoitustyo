from sprites.spaceship import *
from sprites.space import Space
from sprites.shot import *
from sprites.blob import *
from sprites.blocker import Blocker
from sprites.basicenemy import *
from sprites.explosion import *
import pygame


class Level:
    def __init__(self, level_map, cell_size):
        self.cell_size = cell_size
        self.ship = None
        self.spaces = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.shots = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.enemy = None
        self.blobs = pygame.sprite.Group()
        self.gamespeed = 0.5
        self.score = 0

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
                elif cell == 3:
                    self.enemies.add(Basicenemy(normalized_x, normalized_y))
                    #self.enemy = Basicenemy(normalized_x, normalized_y)

        #elf.all_sprites.add(self.spaces, self.walls, self.ship, self.shots)
        self.all_sprites.add(self.walls, self.explosions, self.enemies, self.ship, self.shots)

    def ship_can_move(self, dx=0, dy=0):
        # move ship to new position
        self.ship.rect.move_ip(dx, dy)
        # check if robot hits boundary
        colliding_walls = pygame.sprite.spritecollide(
            self.ship, self.walls, False)
        can_move = not colliding_walls
        # move ship back to original position
        self.ship.rect.move_ip(-dx, -dy)
        return can_move

    def update(self, current_time):
        #ship alive things
        self.ship_got_hit()

        #shots
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
        #enemies
        if len(self.enemies) != 0:
            self.enemy_got_hit(current_time)
        if len(self.enemies) != 0:
            #print(self.enemies)
            #print(len(self.enemies))
            for enemy in self.enemies:
                self.enemy_blob(enemy, current_time)
                if enemy.should_move(current_time):
                    self.move_enemy(enemy)
                    enemy.previous_move_time = current_time

        #effects
        if len(self.explosions) != 0:
            for exp in self.explosions:
                if exp.can_fade(current_time) == True:
                    pygame.sprite.Sprite.kill(exp)
                    #self.explosions.remove(exp)
                    #self.all_sprites.remove(exp)


    def move_ship(self, dx=0, dy=0):
        if not self.ship_can_move(dx, dy):
            return
        self.ship.rect.move_ip(dx, dy)

    def move_shot(self, shot):
        shot.rect.move_ip(0, -10*self.gamespeed)

    def shoot(self, ship, current_time):
        if not ship.can_shoot(current_time):
            return False
        ship.previous_shot_time = current_time
        coords = ship.give_coords()
        new_shot = Shot(coords[0], coords[1])
        self.shots.add(new_shot)
        self.all_sprites.add(self.shots)
        return True
    
    def ship_got_hit(self):
        is_hit = pygame.sprite.spritecollide(self.ship, self.blobs, True)
        if is_hit:
            self.ship.health = self.ship.health - 1
            print("U GOT HIT")
        #if self.ship.is_dead():
            #self.ship_is_kill()
        
    def ship_is_kill(self):
        is_dead = self.ship.is_dead()
        if is_dead == True:
            #print("GAME_OVER")
            return True
        else:
            return False
    

    #score and hp
    def draw_hp_bar(self, display):
        location = (self.ship.rect.x, self.ship.rect.y, 0, 0)
        pygame.draw.rect(display, (255,0,0), (location[0], location[1] - 20, 50, 15))
        pygame.draw.rect(display, (0,128,0), (location[0], location[1] - 20, 50 - (10 * (5 - self.ship.health)), 15))
    
    def draw_score(self, display):
        location = pygame.display.get_window_size()
        font = pygame.font.SysFont("Arial", 36)
        x = location[0]/20
        y = location[1]/20
        text = font.render(str(self.score), True, (255, 0, 0))
        wid = 100
        height = 50
        pygame.draw.rect(display, (0,0,255), (x-10, y-10, wid+20, height+20))
        pygame.draw.rect(display, (0,0,0), (x, y, wid, height))
        display.blit(text, (x+(wid/10), y))


    #enemy actions

    def move_enemy(self, dx=0, dy=0):
        dx = 4*self.gamespeed
        dy = 0
        for enemy in self.enemies:
            if not self.enemy_can_move(enemy, enemy.movedir*dx, enemy.movedir*dy):
                enemy.movedir = enemy.movedir*(-1)
                return
            enemy.rect.move_ip(enemy.movedir*dx, enemy.movedir*dy)

    def enemy_can_move(self,enemy, dx=0, dy=0):
        # move ship to new position
        enemy.rect.move_ip(dx, dy)
        # check if robot hits boundary
        colliding_walls = pygame.sprite.spritecollide(
            enemy, self.walls, False)
        can_move = not colliding_walls
        # move ship back to original position
        enemy.rect.move_ip(-dx, -dy)
        return can_move

    def enemy_got_hit(self, current_time):
        #colliding_shots = pygame.sprite.groupcollide(self.enemies, self.shots, True, True)
        #colliding_enemies = pygame.sprite.groupcollide(self.shots, self.enemies, True, True)
        #remove enemy, add explosion on hit
        #print(colliding_shots)
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
            #remove hit enemy
            for enemy in colliding_enemies:
                for e in enemy:
                    coords.append(e.give_coords())
                    #pygame.sprite.Sprite.remove(e, self.all_sprites, self.enemies)
                    pygame.sprite.Sprite.kill(e)
                    self.score = self.score + 1
                    #self.enemies.remove(e)
            #self.all_sprites.remove(self.enemy)
            #self.enemy = None
            #remove hit shot
            for shot in colliding_shots:
                for s in shot:
                    #self.all_sprites.remove(s)
                    #pygame.sprite.Sprite.remove(s, self.all_sprites, self.shots)
                    pygame.sprite.Sprite.kill(s)
                    #self.shots.remove(s)
            #print(coords)
            #add explosion effect
            for coord in coords:
                new_exp = Explosion(coord[0], coord[1], current_time)
                self.explosions.add(new_exp)
                self.all_sprites.add(self.explosions)
            #print(self.explosions)

    def move_blob(self, blob):
        blob.rect.move_ip(0, self.gamespeed*5)

    def enemy_blob(self, enemy, current_time):
        if not enemy.can_shoot(current_time):
            return False
        enemy.previous_shot_time = current_time
        coords = enemy.give_coords()
        new_blob = Blob(coords[0], coords[1])
        self.blobs.add(new_blob)
        self.all_sprites.add(self.blobs)
        return True