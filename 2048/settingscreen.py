import sys
import pygame
from settings import Settings

class SettingScreen:
    def __init__(self,game):
        super().__init__()
        self.mainscreen = game.screen
        self.settings = game.settings
        margin = 50
        self.x = margin
        self.y = margin
        self.option_button = []
        self.screen_width = game.settings.screen_width - margin*2
        self.screen_height = game.settings.screen_height - margin*2
        self.screen_rect = (self.x, self.y, self.screen_width, self.screen_height)

    def show_screen(self):
        while True:
            stop = self._check_events()
            self._update_screen()
            if stop: break

    def _update_screen(self):
        self.mainscreen.fill(self.settings.bg_color)
        pygame.draw.rect(self.mainscreen, (233,233,233), pygame.Rect(self.screen_rect),False,15)
        self._show_option()
        pygame.display.flip()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                buttonPressed = pygame.mouse.get_pressed()
                if buttonPressed[0]:
                    cursor_pos = pygame.mouse.get_pos()
                    if self.option_button[6].collidepoint(cursor_pos):
                        return True
                    elif self.option_button[0].collidepoint(cursor_pos):
                        self.settings._victory_point = 16
                    elif self.option_button[1].collidepoint(cursor_pos):
                        self.settings._victory_point = 2048
                    elif self.option_button[2].collidepoint(cursor_pos):
                        self.settings._victory_point = 4096
                    elif self.option_button[3].collidepoint(cursor_pos):
                        self.settings.grid_size = 2
                    elif self.option_button[4].collidepoint(cursor_pos):
                        self.settings.grid_size = 4
                    elif self.option_button[5].collidepoint(cursor_pos):
                        self.settings.grid_size = 8


    def _show_option(self):
        self._draw_whatever("CHOOSE ACHIVEMENT:",self.settings.screen_width//2 - 120//2, self.y + 10, 120, 60)
        self._draw_option_box(self.settings.screen_width//2 - 120//2, self.y + 90, 120, 60, "16", 1)
        self._draw_option_box(self.settings.screen_width//2 - 120//2, self.y + 160, 120, 60, "2048", 1)
        self._draw_option_box(self.settings.screen_width//2 - 120//2, self.y + 230, 120, 60, "4096", 1)

        self._draw_whatever("CHOOSE SIZE:",self.settings.screen_width//2 - 120//2, self.y + 300,120,60)
        self._draw_option_box(self.settings.screen_width // 2 - 120 // 2, self.y + 380, 120, 60, "2",3)
        self._draw_option_box(self.settings.screen_width // 2 - 120 // 2, self.y + 450, 120, 60, "4",3)
        self._draw_option_box(self.settings.screen_width // 2 - 120 // 2, self.y + 520, 120, 60, "8",3)

        self._draw_option_box(self.settings.screen_width - self.x - 110,
                              self.settings.screen_height - self.y - 110 , 60, 60, "PLAY",2)

    def _draw_option_box(self, x, y, box_width, box_height, number,color_num):
        option_box_color = {1: (246, 124, 96),
                            2: (150, 90, 70),
                            3: (238, 199, 82)}
        box = pygame.Rect(x, y, box_width, box_height)

        self.option_button.append(box)
        pygame.draw.rect(self.mainscreen, option_box_color[color_num],
                         box, False, 15)
        self._draw_whatever(number, x, y, box_width, box_height)

    def _draw_whatever(self, message, x, y, rect_width, rect_height,size = 30):
        tempFont = pygame.font.SysFont('clear sans', size, bold=True)
        number = tempFont.render(str(message), True, (10, 10, 10))
        numberRect = number.get_rect()
        numberRect.center = (x + rect_width//2, y + rect_height//2)
        self.mainscreen.blit(number, numberRect)

