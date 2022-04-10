import pygame


class GameLoop:
    def __init__(self, level, renderer, event_queue, clock, cell_size):
        self._level = level
        self._renderer = renderer
        self._event_queue = event_queue
        self._clock = clock
        self._cell_size = cell_size

        self.down = False
        self.up = False
        self.right = False
        self.left = False
        self.shoot = False

    def start(self):
        while True:
            if self._handle_events() is False:
                break

            # time
            current_time = self._clock.get_ticks()
            self._level.update(current_time)

            game_over = self._level.ship_is_kill()
            # print(game_over)
            if game_over is True:
                self._renderer.game_over()
                # break
                continue

            if self.shoot is True:
                time = self._clock.get_ticks()
                self._level.shoot(self._level.ship, time)
            if self.up is True:
                self._level.move_ship(diff_y=-self._cell_size)
            if self.down is True:
                self._level.move_ship(diff_y=self._cell_size)
            if self.left is True:
                self._level.move_ship(diff_x=-self._cell_size)
            if self.right is True:
                self._level.move_ship(diff_x=self._cell_size)

            self._render()

            # framerate is n
            self._clock.tick(60)

    def _handle_events(self):
        #pygame.key.set_repeat(1, 100)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    # print("test")
                    self.right = True
                if event.key == pygame.K_LEFT:
                    self.left = True
                if event.key == pygame.K_DOWN:
                    self.down = True
                if event.key == pygame.K_UP:
                    self.up = True
                if event.key == pygame.K_SPACE:
                    self.shoot = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.right = False
                if event.key == pygame.K_LEFT:
                    self.left = False
                if event.key == pygame.K_DOWN:
                    self.down = False
                if event.key == pygame.K_UP:
                    self.up = False
                if event.key == pygame.K_SPACE:
                    self.shoot = False

            elif event.type == pygame.QUIT:
                return False

    def _render(self):
        self._renderer.render()
