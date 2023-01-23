import pygame

class Timer(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/sponsorWoursPNG.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.image = pygame.transform.rotate(self.image, 90)
        self.image = pygame.transform.scale(self.image, (504, 151))
        # self.image.fill((255, 255, 255, 99), None, pygame.BLEND_RGBA_MULT)
        self.rect.center = [x, y]