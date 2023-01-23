import pygame
import random

# Viruses class
class Viruses(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/virus " + str(random.randint(1, 3)) + ".png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (63, 63))
        self.image = pygame.transform.rotate(self.image, 180)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.move_count = 0
        self.move_dir = 1

    def update(self):
        self.rect.y += self.move_dir
        self.move_count += 1
        if abs(self.move_count) > int(75 / 2):
            self.move_dir *= -1
            self.move_count *= self.move_dir