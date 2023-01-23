import pygame
import random
from pygame.locals import *
import cv2 as cv
import numpy as np

import Game

# pygame.mixer.pre_init(44100,-16,2,512)
# mixer.init()
pygame.init()



# fps
clock = pygame.time.Clock()
fps = 30


# #load sounds
# explosion_fx = pygame.mixer.Sound("sounds/exp.wav")
# explosion_fx.set_volume(1.25)
# laser_fx = pygame.mixer.Sound("sounds/laser.wav")
# laser_fx.set_volume(0.25)
# #gamevariables




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

flags = FULLSCREEN | SCALED | DOUBLEBUF
game = Game.Game(flags)




game.create_viruses()
game.spaceship_group.add(game.spaceship)
game.sponsor_group.add(game.sponsor)

cap = cv.VideoCapture(0)
fourcc = cv.VideoWriter_fourcc(*'XVID')
out = cv.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
run = True

while run and cap.isOpened():
    _, img = cap.read()
    clock.tick(fps)
    # draw bg
    game.draw_bg()

    mask_img = skinmask(img)
    contours, hull = getcnthull(mask_img)
    cv.drawContours(img, [contours], -1, (255, 255, 0), 2)
    cv.drawContours(img, [hull], -1, (0, 255, 255), 2)
    centroid = getCentroid(contours)
    area = getArea(contours)
    out.write(img)

    game.update(area, centroid)


    # event handlres
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # result = cv.cvtColor(img, cv.COLOR_RGB2BGR)
    cv.imshow("Camera Input", img)

    # surf = pygame.surfarray.make_surface(img)
    # screen.blit(surf, (0, 0))

    pygame.display.update()
    if cv.waitKey(1) & 0xFF == ord('q'): break

cv.destroyAllWindows()
pygame.quit()
