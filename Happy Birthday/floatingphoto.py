import pygame

class Image:
    def __init__(self,hp):
        super().__init__()
        self.screen = hp.screen
        self.screenrect = hp.screen.get_rect()
        self.image = pygame.image.load('assets/Thinh_with_hat_small.png')
        self.imagerect = self.image.get_rect()
        self.direction_ox = 1
        self.direction_oy = 1
        self.imagerect.x = self.imagerect.width
        self.imagerect.y = self.imagerect.height

    def set_image_and_startpos(self,img_location = 'assets/small_butterfly2.png',x = 1,y = 1,dir_x = 1,dir_y = 1):
        self.image = pygame.image.load(img_location)
        self.imagerect.x = x
        self.imagerect.y = y
        self.direction_ox = dir_x
        self.direction_oy = dir_y

    def check_edge_hit(self):
        if self.imagerect.right >= self.screenrect.right or self.imagerect.left < 0:
            self.direction_ox *= -1
        if self.imagerect.bottom >= self.screenrect.bottom or self.imagerect.top < 0:
            self.direction_oy *= -1

    def _draw_img(self):
        self.screen.blit(self.image, self.imagerect)

    def _update_img(self):
        self.check_edge_hit()
        self.imagerect.x += 1 * self.direction_ox
        self.imagerect.y += 1 * self.direction_oy