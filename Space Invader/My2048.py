import pygame
import sys
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from background import BackGround

class SpaceInvader:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width,
                                               self.settings.screen_height))
        # self.backGround = BackGround(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        pygame.display.set_caption("Space Invader")

    def run(self):
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_alien()
            self._update_screen()

    def _create_fleet(self):
        alien = Alien(self)
        alien_width = alien.rect.width
        alien_height = alien.rect.height
        available_space_x = self.settings.screen_width - (2 * alien_width)
        available_space_y = self.settings.screen_height - 3 * alien_height - self.ship.rect.height
        alien_amount = available_space_x // (2 * alien_width)
        row_amount = available_space_y // (2 * alien_height)

        for j in range(row_amount):
            for i in range(alien_amount):
                self._create_alien(i,j)


    def _create_alien(self,alien_number,row_number):
        alien = Alien(self)
        alien_width = alien.rect.width
        alien_height = alien.rect.height
        init_pos_x = alien_width + 2 * alien_width * alien_number
        init_pos_y = alien_height + 2 * alien_height * row_number
        alien.rect.x = init_pos_x
        alien.rect.y = init_pos_y
        self.aliens.add(alien)

    def _check_fleet_edge(self):
        for alien in self.aliens.sprites():
            if alien.check_edge_hit():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        collision = pygame.sprite.groupcollide(self.bullets,self.aliens,False,True)
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()

        # print(len(self.bullets))

    def _update_alien(self):
        self._check_fleet_edge()
        self.aliens.update()

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        # self.backGround.draw()
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)
        pygame.display.flip()

    def _fire_bullet(self):
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_event(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_event(event)

    def _check_keydown_event(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_event(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False






