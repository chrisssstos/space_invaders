import mediapipe as mp
import cv2 as cv
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return img

    def checkHands(self):
        if self.results.multi_hand_landmarks and len(self.results.multi_hand_landmarks) > 1:
            return True
        else:
            return False

    def findPosition(self, img, handNo, draw=True):

        lmList = []
        #handlen = len(self.results.multi_hand_landmarks)

        if self.checkHands():
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id, cx, cy)
                lmList.append([id, cx, cy])
                if draw:
                    if handNo == 0:
                        cv.circle(img, (cx, cy), 10, (255, 0, 255), cv.FILLED)
                    else:
                        cv.circle(img, (cx, cy), 10, (0, 0, 255), cv.FILLED)

        return lmList

    def centroid(self, vertexes):
        _x_list = [vertex[0] for vertex in vertexes]
        _y_list = [vertex[1] for vertex in vertexes]
        _len = len(vertexes)
        _x = sum(_x_list) / _len
        _y = sum(_y_list) / _len
        return (_x, _y)

    def getCentroidFingers(self, points):
        polygon_data = ((points[8][1],points[8][2]), (points[12][1],points[12][2]), (points[16][1],points[16][2]))
        return self.centroid(polygon_data)

    def getPalm(self, points):
        polygon = Polygon([(points[4][1], points[4][2]), (points[8][1], points[8][2]), (points[12][1], points[12][2]), (points[16][1], points[16][2]), (points[20][1], points[20][2]), (points[0][1], points[0][2])])
        return polygon

    def inShape(self, centroid, polygon):
        point = Point(centroid[0], centroid[1])
        return polygon.contains(point)

    def getPosition(self, palm1, palm2):
        if self.checkHands():
            pos_data = (palm1.centroid.coords[0], palm2.centroid.coords[0])
            return self.centroid(pos_data)







