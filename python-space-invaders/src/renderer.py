import pygame


class Renderer:
    def __init__(self, display, level, bg):
        self._display = display
        self._level = level
        self._bg = bg

    def render(self):
        self._display.blit(self._bg, (0, 0))
        self._level.all_sprites.draw(self._display)
        self._level.draw_hp_bar(self._display)
        self._level.draw_score(self._display)

        pygame.display.update()
    
    def game_over(self):
        tubel = pygame.display.get_window_size()
        font = pygame.font.SysFont("Arial", 48)
        text = font.render("GAME OVER", True, (255, 0, 0))
        self._display.fill((0, 0, 0))
        self._display.blit(text, (int(tubel[0]/3), int(tubel[1]/2)))
        pygame.display.update()
