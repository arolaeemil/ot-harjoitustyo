import pygame
from high_scorehandler import make_record_handler

class Renderer:
    def __init__(self, display, level, background):
        self._display = display
        self._level = level
        self._background = background
        self.is_over = 0
        self.record_handler = make_record_handler()

    def render(self):
        """updates screen
        """
        self._display.blit(self._background, (0, 0))
        self._level.all_sprites.draw(self._display)
        self._level.draw_hp_bar(self._display)
        self._level.draw_score(self._display)
        pygame.display.update()

    def game_over(self):
        """creates the game over screen with score, gets old highscore from database
        and saved new score to database
        """
        tubel = pygame.display.get_window_size()
        font = pygame.font.SysFont("Arial", 48)
        text = font.render("GAME OVER", True, (255, 0, 0))
        self._display.fill((0, 0, 0))
        self._display.blit(text, (int(tubel[0]/3), int(tubel[1]/2)))
        if self.is_over == 0:
            self._level.save_scoredb()
        self.is_over = 1
        score = self._level.score
        old_record = self.record_handler.find_high_score()
        best = old_record[0]
        if score < best:
            scoretext = font.render(
                "score: " + str(score) + ", best score this far is " + str(best), True, (255, 0, 0))
        if score >= best:
            scoretext = font.render(
                "score: " + str(score) + ", it is the new record ", True, (255, 0, 0))
        self._display.blit(scoretext, (int(tubel[0]/3), int(tubel[1]/3)))
        pygame.display.update()
        