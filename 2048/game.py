import pygame
import sys
from settings import Settings
from gameplay import Gameplay
from settingscreen import SettingScreen
from floatingrect import Floatingrect


class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.myfont = pygame.font.SysFont('clear sans', 50, bold=True)
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width,
                                               self.settings.screen_height))
        self.settingscreen = SettingScreen(self)
        self.floatingrect = Floatingrect(self)
        self.gameplay = Gameplay()
        self.button_pressed_times = 0
        pygame.display.set_caption("2048")

    def run(self):
        self.settingscreen.show_screen()
        self.gameplay.settings = self.settingscreen.settings
        self.gameplay.init_grid()
        # print(self.gameplay.getGrid())
        self.gameplay.next_number()
        not_end = True
        while True:
            self._check_events()
            if self._victory_check():
                if not_end:
                    self._update_screen()
                    not_end = False
                self._print_victory_message()
                continue
            if self._gameover_check():
                if not_end:
                    self._update_screen()
                    not_end = False
                self._print_gameover_message()
                continue
            self._update_screen()

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self._update_floatingrect()
        self._update_grid()
        self._draw_side_screen()
        pygame.display.flip()

    def _update_floatingrect(self):
        self.floatingrect.check_edge_hit()
        self.floatingrect.update()
        self.floatingrect.draw()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self._check_key_down_event(event)

    def _check_key_down_event(self, event):
        if event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_RIGHT:
            self.button_pressed_times += 1
            before_pressed_grid = self.gameplay.get_grid()
            self.gameplay.move_event(key='r')
            if not self.gameplay.is_the_same(before_pressed_grid):
                self.gameplay.next_number()

        elif event.key == pygame.K_LEFT:
            self.button_pressed_times += 1
            before_pressed_grid = self.gameplay.get_grid()
            self.gameplay.move_event(key='l')
            if not self.gameplay.is_the_same(before_pressed_grid):
                self.gameplay.next_number()

        elif event.key == pygame.K_UP:
            self.button_pressed_times += 1
            before_pressed_grid = self.gameplay.get_grid()
            self.gameplay.move_event(key='u')
            if not self.gameplay.is_the_same(before_pressed_grid):
                self.gameplay.next_number()

        elif event.key == pygame.K_DOWN:
            self.button_pressed_times += 1
            before_pressed_grid = self.gameplay.get_grid()
            self.gameplay.move_event(key='d')
            if not self.gameplay.is_the_same(before_pressed_grid):
                self.gameplay.next_number()

    def _update_grid(self):
        self.draw_grid(self.screen, self.gameplay.get_grid())

    def draw_grid(self, screen, matrix):
        space = 10
        radius = 10
        width = self.settings.screen_height
        height = width
        for i in range(self.settings.grid_size):
            for j in range(self.settings.grid_size):
                temp = matrix[i][j]
                rect_height = (height - (self.settings.grid_size + 1) * space) / self.settings.grid_size
                rect_width = (width - (self.settings.grid_size + 1) * space) / self.settings.grid_size

                x = j * (rect_width + space) + space
                y = i * (rect_height + space) + space

                # vẽ hình vuống có màu tương ứng với số
                pygame.draw.rect(screen,
                                 self.settings.number_color.get(temp),
                                 pygame.Rect(x, y, rect_width, rect_height), False, radius)

                # thêm viền cho ô vuống
                pygame.draw.rect(screen,
                                 (10, 10, 10),
                                 pygame.Rect(x, y, rect_width, rect_height), True, radius)
                # in số ở ô vuông tương ứng
                self.draw_number(temp, x, y, rect_width, rect_height)

    def draw_number(self, temp, x, y, rect_width, rect_height):
        if temp == 0:
            temp = ''
        number = self.myfont.render(str(temp), True, (10, 10, 10))
        number_rect = number.get_rect()
        number_rect.center = (x + rect_height // 2, y + rect_width // 2)
        self.screen.blit(number, number_rect)

    # kiểm tra xem đã đạt được con số mục tiêu hay chưa
    def _victory_check(self):
        if self.gameplay.grid.__contains__(self.settings.get_victory_point()):
            return True
        return False

    def _print_victory_message(self):
        temp_font = pygame.font.SysFont('clear sans', 80, bold=True)
        message = temp_font.render("YOU WIN!!!", True, (10, 10, 10))
        message_rect = message.get_rect()
        message_rect.center = (self.settings.screen_height // 2, self.settings.screen_height // 2)
        self.screen.blit(message, message_rect)
        pygame.display.flip()

    # kiểm tra xem còn điều kiện kết thúc game
    def _gameover_check(self):
        for i in range(self.settings.grid_size):
            row = self.gameplay.grid[i, :]
            col = self.gameplay.grid[:, i]
            for j in range(len(row) - 1):
                if row[j] == row[j + 1] or row[j] == 0 or row[j + 1] == 0:
                    return False
            for j in range(len(col) - 1):
                if col[j] == col[j + 1] or col[j] == 0 or col[j + 1] == 0:
                    return False
        return True

    def _print_gameover_message(self):
        temp_font = pygame.font.SysFont('clear sans', 60, bold=False)
        message = temp_font.render("OUT OF MOVES, GAME OVER !!!", True, (10, 10, 10))
        message_rect = message.get_rect()
        message_rect.center = (self.settings.screen_height // 2, self.settings.screen_height // 2)
        self.screen.blit(message, message_rect)
        pygame.display.flip()

    def _draw_side_screen(self):
        remain = self.settings.screen_width - self.settings.screen_height
        self.print_message("Destination: " + str(self.settings.get_victory_point()), self.settings.screen_width - remain//2, 50)
        self.print_message("Button pressed: " + str(self.button_pressed_times) + " times", self.settings.screen_width - remain//2, 100)
        self.print_message("q: Exit Game", self.settings.screen_width - remain//2, self.settings.screen_height - 50)

    def print_message(self, message, x, y):
        temp_font = pygame.font.SysFont('clear sans', 40, bold=False)
        message = temp_font.render(str(message), True, (10, 10, 10))
        message_rect = message.get_rect()
        message_rect.center = (x, y)
        self.screen.blit(message, message_rect)