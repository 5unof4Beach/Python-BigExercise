import pygame.image
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self,ai_game):
        super().__init__()
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.image = pygame.image.load('assets/small_butterfly2.png')
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)
        self.speed = 1.0

    def update(self):
            self.rect.x += self.settings.alien_speed * self.settings.fleet_direction

    def check_edge_hit(self):
        if self.rect.right >= self.screen_rect.right or self.rect.left < 0:
            return True

