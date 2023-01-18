import math

import cv2
import numpy

import mediapipe as mp


class poseDetector():
    def __init__(self):
        self.lmList = None
        self.results = None
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(min_detection_confidence=0.7)
    
    def findLandmarks(self, img):
        """
        :param img: The image to process
        :return: A list of landmarks each element contains if the
        landmark is visible in the image, the id of the landmark and
         the coordinates of the landmark
        """
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            self.lmList = []
            h, w, c = img.shape
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                # print(id, lm)
                cx, cy = int(lm.x * w), int(lm.y * h)
                test = (cx in range(0, w)) and (cy in range(0, h))
                self.lmList.append([test, id, cx, cy])

        return self.lmList
    
    def findPose(self, img: numpy.ndarray, draw: bool = True) -> numpy.ndarray:
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,
                                           self.mpPose.POSE_CONNECTIONS)
        return img

    def findPosition(self, img: numpy.ndarray, draw: bool = True) -> list:
        self.lmList = []
        if self.results.pose_landmarks:
            h, w, c = img.shape
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                # print(id, lm)
                cx, cy = int(lm.x * w), int(lm.y * h)
                test = (cx in range(0, w)) and (cy in range(0, h))
                self.lmList.append([test, id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, f'{id}', (cx, cy), cv2.FONT_HERSHEY_PLAIN, 1,
                                (255, 0, 0), 1)

        return self.lmList

    def inPicture(self, img: numpy.ndarray) -> str:
        if len(self.lmList) == 0:
            return "Step In Front Of The Camera"
        else:
            for i in range(33):
                if self.lmList[i][0] == False:
                    return 'Step Back Until Your Whole Body Is In The Picture'
            return "Follow The Pose At The Top Left"

    def findAngle(self, p1: int, p2: int, p3: int) -> float:
        """
        :param p1: point1 id
        :param p2: point2 id
        :param p3: point3 id
        :return: the angle between the 3 input points
        """
        # Get the landmarks
        x1, y1 = self.lmList[p1][2:]
        x2, y2 = self.lmList[p2][2:]
        x3, y3 = self.lmList[p3][2:]
        # Calculate the Angle
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                             math.atan2(y1 - y2, x1 - x2))
        if angle == 0:
            angle += 360

        return angle
