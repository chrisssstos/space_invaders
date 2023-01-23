import pygame
import random
from pygame.locals import *
import cv2 as cv
import numpy as np

import Spaceship
import Sponsor
import Viruses
import Bullets

class Game():
    def __init__(self,flags):


        self.screen_w = 960
        self.screen_h = 540

        self.screen = pygame.display.set_mode((self.screen_w, self.screen_h), flags, 8)
        self.bg = pygame.image.load("img/space.png").convert_alpha()
        pygame.display.set_caption('Invaders')
        # define fonts
        self.font40 = pygame.font.Font("pixel_font.font", 60)

        self.rows = 6
        self.cols = 7
        self.countdown = 3
        self.time = 0
        self.kills = 0
        self.posW = 0
        self.cntW = int(150 / 2)
        self.cntW2 = int(150 / 2)
        self.cntWW2 = int(300 / 2)
        self.time_add = pygame.time.get_ticks()
        self.last_count = pygame.time.get_ticks()
        self.timerStop = False
        self.game_over = 0  # 0 no gme over,1 win
        self.away = False

        # define colors
        self.red = (255, 0, 0)
        self.reen = (0, 255, 0)
        self.pink = (255, 120, 194)
        self.white = (255, 255, 255)
        self.yellow = (255, 255, 0)

        # create sprite groups
        self.spaceship_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.virus_group = pygame.sprite.Group()
        self.explosion_group = pygame.sprite.Group()
        self.sponsor_group = pygame.sprite.Group()

        # create player
        self.spaceship = Spaceship.Spaceship(int(self.screen_w - 128), int(self.screen_h / 2), 3)

        self.sponsor = Sponsor.Sponsor(self.screen_w + (self.screen_w / 2), int(self.screen_h / 2) + (self.screen_h / 4))

    def draw_bg(self):
        self.screen.blit(self.bg, (0, 0))


    def create_viruses(self):
        # gnerate aliens
        for row in range(self.rows):
            for item in range(self.cols):
                virus = Viruses.Viruses(75 + item * 100, 75 + row * 75)
                self.virus_group.add(virus)

    # def function for creating text
    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        img = pygame.transform.rotate(img, 90)
        img = pygame.transform.scale(img, (50, 250))
        self.screen.blit(img, (x, y))

    def draw_text2(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        img = pygame.transform.rotate(img, 90)
        img = pygame.transform.scale(img, (50, 345))
        self.screen.blit(img, (x, y))

    def draw_cnt(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        img = pygame.transform.rotate(img, 90)
        img = pygame.transform.scale(img, (150, self.cntW))
        self.screen.blit(img, (x, y))

    def draw_cnt2(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        img = pygame.transform.rotate(img, 90)
        img = pygame.transform.scale(img, (50, 75))
        self.screen.blit(img, (x, y))

    def draw_cnt3(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        img = pygame.transform.rotate(img, 90)
        img = pygame.transform.scale(img, (self.cntWW2, self.cntW2))
        self.screen.blit(img, (x, y))


    def update(self, area, centroid):
        if self.countdown <= 0:
            # check if all virus kill
            if len(self.virus_group) == 0:
                self.game_over = 1

            if self.game_over == 0:
                # update spaceship
                self.game_over = self.spaceship.update()
                if area > 5000:
                    if centroid > 250 and self.spaceship.rect.bottom < self.screen_h:
                        self.spaceship.rect.y += self.spaceship.speed
                    elif centroid < 250 and self.spaceship.rect.top > 0:
                        self.spaceship.rect.y -= self.spaceship.speed

                time_now = pygame.time.get_ticks()

                if area > 1:
                    #                 laser_fx.play()
                    bullet = Bullets.Bullets(self.spaceship.rect.left, self.spaceship.rect.centery)
                    self.bullet_group.add(bullet)
                    self.spaceship.last_shot = time_now
                    # record current time

                # update sprite groups
                self.bullet_group.update()
                self.virus_group.update()

            count_time = pygame.time.get_ticks()
            if self.timerStop == False:
                if count_time - self.time_add > 1000:
                    self.time += 1
                    self.time_add = count_time
                if self.time > 9:
                    self.cntW = int(300 / 2)
                else:
                    self.cntW = int(150 / 2)
                if self.kills > 9:
                    self.cntW2 = int(300 / 2)
                    self.cntWW2 = int(300 / 2)
                    self.posW = int(100 / 2)
                else:
                    self.cntW2 = int(150 / 2)
                    self.posW = int(10 / 2)

        self.explosion_group.update()

        # update sprite groups
        if self.time > 0 and self.timerStop == False:
            self.draw_cnt(str(self.time), self.font40, self.yellow, int(self.screen_w) - 200, 0 + 10)
            self.draw_cnt3(str(self.kills), self.font40, self.pink, int(self.screen_w) - 200, 540 - 100 - self.posW)
        self.sponsor_group.draw(self.screen)
        self.spaceship_group.draw(self.screen)
        self.bullet_group.draw(self.screen)
        self.virus_group.draw(self.screen)
        print(area)

        if self.game_over == 1:
            self.bullet_group = pygame.sprite.Group()
            self.virus_group = pygame.sprite.Group()
            explosion_group = pygame.sprite.Group()
            self.draw_text('YOU WIN!', self.font40, self.white, int((self.screen_w) - 768 / 2), int((self.screen_h / 2) - 240 / 2))
            self.draw_text2('TIME WASHED:', self.font40, self.white, int((self.screen_w) - 640 / 2), int((self.screen_h / 2) - 240 / 2))
            self.draw_cnt2(str(self.time) + "s", self.font40, self.yellow, int((self.screen_w) - 640 / 2), int((self.screen_h / 2) - 400 / 2))
            self.draw_text2('GERMS KILLED:', self.font40, self.white, int((self.screen_w) - 512 / 2), int((self.screen_h / 2) - 240 / 2))
            self.draw_cnt2(str(self.kills) + " ", self.font40, self.pink, int((self.screen_w) - 512 / 2), int((self.screen_h / 2) - 400 / 2))
            self.timerStop = True
            key = pygame.key.get_pressed()
            if key[pygame.K_r]:
                self.timerStop = False
                self.time = 0
                self.kills = 0
                self.game_over = 0
                self.countdown = 4
                self.create_viruses()

        if self.game_over == 3 or area <= 30000:
            self.draw_bg()
            self.bullet_group = pygame.sprite.Group()
            self.away = True
            self.explosion_group = pygame.sprite.Group()

            self.draw_text('YOU LEFT :(', self.font40, self.white, int((self.screen_w) - 768 / 2), int((self.screen_h / 2) - 240 / 2))
            self.draw_text2('TIME WASHED:', self.font40, self.white, int((self.screen_w) - 640 / 2), int((self.screen_h / 2) - 240 / 2))
            self.draw_cnt2(str(time) + "s ", self.font40, self.yellow, int((self.screen_w) - 640 / 2), int((self.screen_h / 2) - 400 / 2))
            self.draw_text2('GERMS KILLED:', self.font40, self.white, int((self.screen_w) - 512 / 2), int((self.screen_h / 2) - 240 / 2))
            self.draw_cnt2(str(kills) + "  ", self.font40, self.pink, int((self.screen_w) - 512 / 2), int((self.screen_h / 2) - 400 / 2))
            self.timerStop = True

            key = pygame.key.get_pressed()
            if key[pygame.K_r]:
                self.virus_group = pygame.sprite.Group()
                self.timerStop = False
                self.time = 0
                self.kills = 0
                self.game_over = 0
                self.countdown = 4
                self.create_viruses()
        self.explosion_group.draw(self.screen)
        if self.away == True and area > 30000:
            if self.time != 0 and self.kills != 0:
                with open('times.txt', 'a') as t:
                    t.write(str(self.time) + '\n')
                with open('kills.txt', 'a') as t:
                    t.write(str(self.kills) + '\n')
            self.virus_group = pygame.sprite.Group()
            self.timerStop = False
            self.time = 0
            self.kills = 0
            self.game_over = 0
            self.countdown = 4
            self.create_viruses()
            self.away = False

        if self.countdown > 0 and area > 10000:
            self.draw_text('GET READY!', self.font40, self.white, int(self.screen_w - 500 / 2), int(self.screen_h / 2) - int(240 / 2))
            self.draw_cnt(str(self.countdown), self.font40, self.white, int((self.screen_w) - 400 / 2), int(self.screen_h / 2) - int(70 / 2))
            self.count_timer = pygame.time.get_ticks()
            if self.count_timer - self.last_count > 1000:
                self.countdown -= 1
                self.last_count = self.count_timer