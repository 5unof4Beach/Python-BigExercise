import pygame
import sys
from settings import Settings
from gameplay import Gameplay

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.myfont = pygame.font.SysFont('clear sans',50,bold=True)
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width,
                                               self.settings.screen_width))
        self.gameplay = Gameplay()
        self.gameplay.next_number()
        pygame.display.set_caption("2048")

    def run(self):
        while True:
            self._check_events()
            self._update_screen()

    def _update_screen(self):
        while True:
            self._check_events()
            self.screen.fill(self.settings.bg_color)
            self._update_grid()
            self._vitory_check()
            pygame.display.flip()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.quit():
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_key_down_event(event)

    def _check_key_down_event(self,event):
        if event.key == pygame.K_RIGHT:
            before_pressed_grid = self.gameplay.getGrid()
            self.gameplay.move_event(key='r')
            if not self.gameplay.isTheSame(before_pressed_grid):
                self.gameplay.next_number()
        elif event.key == pygame.K_LEFT:
            before_pressed_grid = self.gameplay.getGrid()
            self.gameplay.move_event(key='l')
            if not self.gameplay.isTheSame(before_pressed_grid):
                self.gameplay.next_number()
        elif event.key == pygame.K_UP:
            before_pressed_grid = self.gameplay.getGrid()
            self.gameplay.move_event(key='u')
            if not self.gameplay.isTheSame(before_pressed_grid):
                self.gameplay.next_number()
        elif event.key == pygame.K_DOWN:
            before_pressed_grid = self.gameplay.getGrid()
            self.gameplay.move_event(key='d')
            if not self.gameplay.isTheSame(before_pressed_grid):
                self.gameplay.next_number()

    def _update_grid(self):
        self.draw_grid(self.screen,self.gameplay.getGrid(),self.myfont)

    def draw_grid(self,screen,matrix,font):
        space = 10
        width = self.settings.screen_width
        height = width
        for i in range(self.settings.grid_size):
            for j in range(self.settings.grid_size):
                temp = matrix[i][j]
                x = j * width // self.settings.grid_size + space
                y = i * height // self.settings.grid_size + space
                rect_height = height // self.settings.grid_size - 2 * space
                rect_width = width // self.settings.grid_size - 2 * space
                pygame.draw.rect(screen,
                                 self.settings.number_color.get(temp),
                                 pygame.Rect(x,y,rect_width,rect_height))
                self.draw_number(temp,matrix,x,y,rect_width,rect_height)

    def draw_number(self,temp,matrix,x,y,rect_width,rect_height):
        number = self.myfont.render(str(temp),True,(10,10,10))
        numberRect = number.get_rect()
        numberRect.center = (x + rect_height//2,y + rect_width//2)
        self.screen.blit(number,numberRect)

    def _vitory_check(self):
        if self.gameplay.grid.__contains__(self.settings._victory_point):
            tempFont = pygame.font.SysFont('clear sans',80,bold=True)
            message = tempFont.render("YOU WIN",True,(10,10,10))
            messageRect = message.get_rect()
            messageRect.center = (self.settings.screen_width//2,self.settings.screen_width//2)
            self.screen.blit(message,messageRect)

