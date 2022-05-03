import os
import pygame


class Renderer:
    def __init__(self, display, level, background):
        self._display = display
        self._level = level
        self._background = background
        self.is_over = 0

    def render(self):
        self._display.blit(self._background, (0, 0))
        self._level.all_sprites.draw(self._display)
        self._level.draw_hp_bar(self._display)
        self._level.draw_score(self._display)

        pygame.display.update()

    def game_over(self):
        """creates the game over screen with score
        """
        tubel = pygame.display.get_window_size()
        font = pygame.font.SysFont("Arial", 48)
        text = font.render("GAME OVER", True, (255, 0, 0))
        self._display.fill((0, 0, 0))
        self._display.blit(text, (int(tubel[0]/3), int(tubel[1]/2)))
        if self.is_over == 0:
            self._level.save_score()
        self.is_over = 1
        script_path = os.path.dirname(os.path.abspath(__file__))
        rel_path = "record.txt"
        abs_file_path = os.path.join(script_path, rel_path)
        with open(abs_file_path, "r", encoding="utf-8") as scorefile:
            lines = scorefile.readlines()
            scores = [int(i) for i in lines]
            score = scores[len(lines)-1]
            best = max(scores)
        if score < best:
            scoretext = font.render(
                "score: " + str(score) + ", best score this far is " + str(best), True, (255, 0, 0))
        if score >= best:
            scoretext = font.render(
                "score: " + str(score) + ", it is the new record ", True, (255, 0, 0))
        self._display.blit(scoretext, (int(tubel[0]/3), int(tubel[1]/3)))
        pygame.display.update()
