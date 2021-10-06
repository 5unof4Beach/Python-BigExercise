import pygame.image
from random import randint


class BackGround():
    def __init__(self,ai_game):
        self.settings = ai_game.settings
        self.screen = ai_game.screen
        self.image = pygame.image.load('assets/star_backgorund.png')
        self.rect = self.image.get_rect()

    def draw(self):
        x = randint(0,1200)
        y = randint(0, 800)
        self.rect.x = x
        self.rect.y = y
        self.screen.blit(self.image,self.rect)