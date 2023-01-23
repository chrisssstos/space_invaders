import pygame
import random
from pygame.locals import *
import cv2 as cv
import numpy as np
import Handtracking


# pygame.mixer.pre_init(44100,-16,2,512)
# mixer.init()
pygame.init()

# fps
clock = pygame.time.Clock()
fps = 30

screen_w = 960
screen_h = 540

flags = FULLSCREEN | SCALED | DOUBLEBUF
screen = pygame.display.set_mode((screen_w, screen_h), flags, 8)
pygame.display.set_caption('Invaders')
# define fonts
font40 = pygame.font.Font("pixel_font.font", 60)

# #load sounds
# explosion_fx = pygame.mixer.Sound("sounds/exp.wav")
# explosion_fx.set_volume(1.25)
# laser_fx = pygame.mixer.Sound("sounds/laser.wav")
# laser_fx.set_volume(0.25)
# #gamevariables
rows = 6
cols = 7
countdown = 3
time = 0
kills = 0
posW = 0
cntW = int(150 / 2)
cntW2 = int(150 / 2)
cntWW2 = int(300 / 2)
time_add = pygame.time.get_ticks()
last_count = pygame.time.get_ticks()
timerStop = False
game_over = 0  # 0 no gme over,1 win
away = False
# define colors
red = (255, 0, 0)
green = (0, 255, 0)
pink = (255, 120, 194)
white = (255, 255, 255)
yellow = (255, 255, 0)

bg = pygame.image.load("img/space.png").convert_alpha()


def draw_bg():
    screen.blit(bg, (0, 0))


# def function for creating text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    img = pygame.transform.rotate(img, 90)
    img = pygame.transform.scale(img, (50, 250))
    screen.blit(img, (x, y))


def draw_text2(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    img = pygame.transform.rotate(img, 90)
    img = pygame.transform.scale(img, (50, 345))
    screen.blit(img, (x, y))


def draw_cnt(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    img = pygame.transform.rotate(img, 90)
    img = pygame.transform.scale(img, (150, cntW))
    screen.blit(img, (x, y))


def draw_cnt2(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    img = pygame.transform.rotate(img, 90)
    img = pygame.transform.scale(img, (50, 75))
    screen.blit(img, (x, y))


def draw_cnt3(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    img = pygame.transform.rotate(img, 90)
    img = pygame.transform.scale(img, (cntWW2, cntW2))
    screen.blit(img, (x, y))


def skinmask(img):
    hsvim = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    lower = np.array([0, 2, 10], dtype="uint8")
    upper = np.array([20, 255, 255], dtype="uint8")
    skinRegionHSV = cv.inRange(hsvim, lower, upper)
    blurred = cv.blur(skinRegionHSV, (2, 2))
    ret, thresh = cv.threshold(blurred, 0, 255, cv.THRESH_BINARY)
    return thresh


def getcnthull(mask_img):
    contours, hierarchy = cv.findContours(mask_img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    contours = max(contours, key=lambda x: cv.contourArea(x))
    hull = cv.convexHull(contours)
    return contours, hull


def getArea(contours):
    area = cv.contourArea(contours)
    return area


def getCentroid(contours):
    moments = cv.moments(contours)
    cx = int(moments["m10"] / moments["m00"])
    cy = int(moments["m01"] / moments["m00"])
    return cx



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
            self.rect.y -= speed
        if key[pygame.K_UP] and self.rect.bottom < screen_h:
            self.rect.y += speed

        # record current time
        time_now = pygame.time.get_ticks()
        # shoot
        if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
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


class Sponsor(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/sponsorWoursPNGWHITEBIG2.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.image = pygame.transform.rotate(self.image, 90)
        self.image = pygame.transform.scale(self.image, (86, 212))
        # self.image.fill((255, 255, 255, 99), None, pygame.BLEND_RGBA_MULT)
        self.rect.center = [x, y]


class Timer(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/sponsorWoursPNG.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.image = pygame.transform.rotate(self.image, 90)
        self.image = pygame.transform.scale(self.image, (504, 151))
        # self.image.fill((255, 255, 255, 99), None, pygame.BLEND_RGBA_MULT)
        self.rect.center = [x, y]


# class Bullets2(pygame.sprite.Sprite):
#     def __init__(self,x,y):
#         pygame.sprite.Sprite.__init__(self)
#         self.image = pygame.image.load("img/bullet.png").convert_alpha()
#         self.rect = self.image.get_rect()
#         self.rect.center = [x,y]
#
#     def update(self):
#         self.rect.y +=5
#         if self.rect.top>screen_h:
#             self.kill()
#         if pygame.sprite.spritecollide(self,virus_group, True):
#             self.kill()
#             explosion = Explosion(self.rect.centerx,self.rect.centery+63,1)
#             explosion_group.add(explosion)


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


# explosion class
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(0, 6):
            img = pygame.image.load(f"img/explosion/explosion_{num}.png").convert_alpha()
            if size == 1:
                img = pygame.transform.scale(img, (50, 50))
            # add to list
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        explosion_speed = 3
        # update anim
        self.counter += 1
        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()


# create sprite groups
spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
virus_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
sponsor_group = pygame.sprite.Group()


def create_viruses():
    # gnerate aliens
    for row in range(rows):
        for item in range(cols):
            virus = Viruses(75 + item * 100, 75 + row * 75)
            virus_group.add(virus)


create_viruses()

# create player
spaceship = Spaceship(int(screen_w - 128), int(screen_h / 2), 3)
spaceship_group.add(spaceship)

sponsor = Sponsor(screen_w + (screen_w / 2), int(screen_h / 2) + (screen_h / 4))
sponsor_group.add(sponsor)
detector = Handtracking.handDetector()

cap = cv.VideoCapture(0)
fourcc = cv.VideoWriter_fourcc(*'XVID')
out = cv.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
run = True

posX = 0


while run and cap.isOpened():
    shootBullet = False
    _, img = cap.read()
    clock.tick(fps)
    # draw bg
    draw_bg()

    mask_img = skinmask(img)
    contours, hull = getcnthull(mask_img)
    cv.drawContours(img, [contours], -1, (255, 255, 0), 2)
    cv.drawContours(img, [hull], -1, (0, 255, 255), 2)
    centroid = getCentroid(contours)
    area = getArea(contours)
    out.write(img)


    height, width, c = img.shape

    img = detector.findHands(img)
    lmList1 = detector.findPosition(img, 0)
    lmList2 = detector.findPosition(img, 1)


    if len(lmList1) != 0:
        center1 = detector.getCentroidFingers(lmList1)
        center2 = detector.getCentroidFingers(lmList2)
        palm1 = detector.getPalm(lmList1)
        palm2 = detector.getPalm(lmList2)

        if detector.inShape(center1, palm2) or detector.inShape(center2, palm1):
            shootBullet = True

        posX = detector.getPosition(palm1, palm2)[0]



    if countdown <= 0:
        # check if all virus kill
        if len(virus_group) == 0:
            game_over = 1

        if game_over == 0:
            # update spaceship
            game_over = spaceship.update()
            if centroid > width/2 and spaceship.rect.bottom < screen_h:
                spaceship.rect.y += spaceship.speed
            elif centroid < width/2 and spaceship.rect.top > 0:
                spaceship.rect.y -= spaceship.speed

            time_now = pygame.time.get_ticks()

            if shootBullet and time_now - spaceship.last_shot > spaceship.cooldown:
                #                 laser_fx.play()
                bullet = Bullets(spaceship.rect.left, spaceship.rect.centery)
                bullet_group.add(bullet)
                spaceship.last_shot = time_now
                # record current time

            # update sprite groups
            bullet_group.update()
            virus_group.update()

        count_time = pygame.time.get_ticks()
        if timerStop == False:
            if count_time - time_add > 1000:
                time += 1
                time_add = count_time
            if time > 9:
                cntW = int(300 / 2)
            else:
                cntW = int(150 / 2)
            if kills > 9:
                cntW2 = int(300 / 2)
                cntWW2 = int(300 / 2)
                posW = int(100 / 2)
            else:
                cntW2 = int(150 / 2)
                posW = int(10 / 2)

    explosion_group.update()

    # update sprite groups
    if time > 0 and timerStop == False:
        draw_cnt(str(time), font40, yellow, int(screen_w) - 200, 0 + 10)
        draw_cnt3(str(kills), font40, pink, int(screen_w) - 200, 540 - 100 - posW)
    sponsor_group.draw(screen)
    spaceship_group.draw(screen)
    bullet_group.draw(screen)
    virus_group.draw(screen)
    #print(area)
    if game_over == 1:
        bullet_group = pygame.sprite.Group()
        virus_group = pygame.sprite.Group()
        explosion_group = pygame.sprite.Group()
        draw_text('YOU WIN!', font40, white, int((screen_w) - 768 / 2), int((screen_h / 2) - 240 / 2))
        draw_text2('TIME WASHED:', font40, white, int((screen_w) - 640 / 2), int((screen_h / 2) - 240 / 2))
        draw_cnt2(str(time) + "s", font40, yellow, int((screen_w) - 640 / 2), int((screen_h / 2) - 400 / 2))
        draw_text2('GERMS KILLED:', font40, white, int((screen_w) - 512 / 2), int((screen_h / 2) - 240 / 2))
        draw_cnt2(str(kills) + " ", font40, pink, int((screen_w) - 512 / 2), int((screen_h / 2) - 400 / 2))
        timerStop = True
        key = pygame.key.get_pressed()
        if key[pygame.K_r]:
            timerStop = False
            time = 0
            kills = 0
            game_over = 0
            countdown = 4
            create_viruses()

    if game_over == 3 or area <= 5000:
        draw_bg()
        bullet_group = pygame.sprite.Group()
        away = True
        explosion_group = pygame.sprite.Group()

        draw_text('YOU LEFT :(', font40, white, int((screen_w) - 768 / 2), int((screen_h / 2) - 240 / 2))
        draw_text2('TIME WASHED:', font40, white, int((screen_w) - 640 / 2), int((screen_h / 2) - 240 / 2))
        draw_cnt2(str(time) + "s ", font40, yellow, int((screen_w) - 640 / 2), int((screen_h / 2) - 400 / 2))
        draw_text2('GERMS KILLED:', font40, white, int((screen_w) - 512 / 2), int((screen_h / 2) - 240 / 2))
        draw_cnt2(str(kills) + "  ", font40, pink, int((screen_w) - 512 / 2), int((screen_h / 2) - 400 / 2))
        timerStop = True

        key = pygame.key.get_pressed()
        if key[pygame.K_r]:
            virus_group = pygame.sprite.Group()
            timerStop = False
            time = 0
            kills = 0
            game_over = 0
            countdown = 4
            create_viruses()
    explosion_group.draw(screen)
    if away == True and area>30000:
        if time != 0 and kills != 0:
            with open('times.txt', 'a') as t:
                t.write(str(time) + '\n')
            with open('kills.txt', 'a') as t:
                t.write(str(kills) + '\n')
        virus_group = pygame.sprite.Group()
        timerStop = False
        time = 0
        kills = 0
        game_over = 0
        countdown = 4
        create_viruses()
        away = False

    if countdown > 0 and detector.checkHands():
        draw_text('GET READY!', font40, white, int(screen_w - 500 / 2), int(screen_h / 2) - int(240 / 2))
        draw_cnt(str(countdown), font40, white, int((screen_w) - 400 / 2), int(screen_h / 2) - int(70 / 2))
        count_timer = pygame.time.get_ticks()
        if count_timer - last_count > 1000:
            countdown -= 1
            last_count = count_timer

    # event handlres
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    cv.imshow("Camera Input", img)

    # surf = pygame.surfarray.make_surface(img)
    # screen.blit(surf, (0, 0))

    pygame.display.update()
    if cv.waitKey(1) & 0xFF == ord('q'): break

cv.destroyAllWindows()
pygame.quit()
