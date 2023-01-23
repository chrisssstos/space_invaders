import pygame
import Explosion

# Bullets class
class Bullets(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/bullet.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.image = pygame.transform.rotate(self.image, 90)
        self.image = pygame.transform.scale(self.image, (25, 25))
        self.rect.center = [x, y]

    def update(self):
        global kills
        self.rect.x -= 8
        if self.rect.bottom < 0:
            self.kill()
        if pygame.sprite.spritecollide(self, virus_group, True):
            kills += 1
            self.kill()
            #             explosion_fx.play()
            explosion = Explosion(self.rect.centerx, self.rect.centery - 31, 1)
            explosion_group.add(explosion)