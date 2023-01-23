import pygame

import Bullets



# spaceship class
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.images = []

        for num in range(0, 5):
            img = pygame.image.load(f"img/spaceship sprite/sprite_{num}.png").convert_alpha()
            img = pygame.transform.scale(img, (128, 128))
            img = pygame.transform.rotate(img, 180)
            # add to list
            self.images.append(img)

        # self.image = pygame.image.load("img/spaceship sprite/sprite_0.png").convert_alpha()
        # self.image = pygame.transform.scale(self.image, (256, 256))
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.health_start = health
        self.health_remaining = health
        self.last_shot = pygame.time.get_ticks()
        self.counter = 0
        self.cooldown = 300
        self.speed = 16

    def update(self):
        # set movement speed and cooldown(in miliseconds)
        animation_speed = 5
        game_over = 0
        # animate
        self.counter += 1
        if self.counter >= animation_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]
        if self.index >= len(self.images) - 1 and self.counter >= animation_speed:
            self.index = 0
            self.counter = 0
        #         #get key press
        key = pygame.key.get_pressed()
        if key[pygame.K_DOWN] and self.rect.top > 0:
            self.rect.y -= self.speed
        if key[pygame.K_UP] and self.rect.bottom < self.screen_h:
            self.rect.y += self.speed

        # record current time
        time_now = pygame.time.get_ticks()
        # shoot
        if key[pygame.K_SPACE] and time_now - self.last_shot > self.cooldown:
            #             laser_fx.play()
            bullet = Bullets(self.rect.left, self.rect.centery)
            bullet_group.add(bullet)
            # bullet2 = Bullets2(self.rect.centerx, self.rect.bottom)
            # bullet_group.add(bullet2)
            self.last_shot = time_now
        if key[pygame.K_a]:
            game_over = 3

        if key[pygame.K_ESCAPE]:
            pygame.quit()

        # draw health bar
        # pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom+10), self.rect.width,15))
        # if self.health_remaining>0:
        #     pygame.draw.rect(screen, green, (self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.health_remaining / self.health_start)), 15))
        return game_over