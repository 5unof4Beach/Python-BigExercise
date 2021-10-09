import pygame
import sys
from floatingphoto import Image


class Birthday:
    def __init__(self):
        pygame.init()
        self.width = 1280
        self.height = 720
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screenrect = self.screen.get_rect()

        self.image_1 = Image(self)
        self.image_2 = Image(self)
        self.image_setter()

        pygame.display.set_caption("Happy Birthday")

    def image_setter(self):
        self.image_1.set_image_and_startpos('assets/Giang_with_hat_small.png', x=50, y=50)
        self.image_2.set_image_and_startpos('assets/Thinh_with_hat_small.png', x=500, y=400, dir_x=1, dir_y=-1)

    def _update_screen(self):
        if self.image_1.imagerect.colliderect(self.image_2.imagerect):
            self.image_1.direction_ox *= -1
            self.image_2.direction_ox *= -1
            self.image_1.direction_oy *= -1
            self.image_2.direction_oy *= -1
        self.screen.fill((187, 173, 160))
        self.image_1._update_img()
        self.image_2._update_img()
        self.image_1._draw_img()
        self.image_2._draw_img()
        self.draw_birthday_mess()
        pygame.display.flip()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            self._update_screen()

    def draw_birthday_mess(self):
        self._draw_whatever("HAPPY 28th BIRTHDAY ", self.width // 2, 50, size=70)
        self._draw_whatever("09 - 10 - 2021", self.width // 2, 100, size=50)

    def _draw_whatever(self, message, x, y, size=30):
        temp_font = pygame.font.SysFont('clear sans', size, bold=True)
        number = temp_font.render(str(message), True, (10, 10, 10))
        number_rect = number.get_rect()
        number_rect.center = (x, y)
        self.screen.blit(number, number_rect)
