import cv2
import mediapipe as mp
import time
import math

import numpy


class poseDetector():
    def __init__(self):
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(min_detection_confidence=0.7)

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

    def findAngle(self, img: numpy.ndarray, p1: int, p2: int, p3: int, draw: bool = True) -> float:
        # Get the landmarks
        x1, y1 = self.lmList[p1][2:]
        x2, y2 = self.lmList[p2][2:]
        x3, y3 = self.lmList[p3][2:]
        # Calculate the Angle
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                             math.atan2(y1 - y2, x1 - x2))
        if angle == 0:
            angle += 360
        # print(angle)
        # Draw
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 2)
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 2)
            cv2.circle(img, (x1, y1), 7, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 10, (0, 0, 255), 2)
            cv2.circle(img, (x2, y2), 7, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (0, 0, 255), 2)
            cv2.circle(img, (x3, y3), 7, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 10, (0, 0, 255), 2)
            cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        return angle


def image_detector(img, detector):
    img1 = img.copy()
    img1 = detector.findPose(img1)
    lmList = detector.findPosition(img, draw=True)
    if len(lmList) != 0:
        point = 11
        cx, cy = lmList[point][2], lmList[point][3]
        cv2.circle(img, (cx, cy), 5, (0, 0, 255), cv2.FILLED)
        point = 23
        cx, cy = lmList[point][2], lmList[point][3]
        cv2.circle(img, (cx, cy), 5, (0, 0, 255), cv2.FILLED)
        point = 25
        cx, cy = lmList[point][2], lmList[point][3]
        cv2.circle(img, (cx, cy), 5, (0, 0, 255), cv2.FILLED)

        point = 7
        cx, cy = lmList[point][2], lmList[point][3]
        cv2.circle(img, (cx, cy), 5, (0, 0, 255), cv2.FILLED)
        point = 9
        cx, cy = lmList[point][2], lmList[point][3]
        cv2.circle(img, (cx, cy), 5, (0, 0, 255), cv2.FILLED)
        point = 10
        cx, cy = lmList[point][2], lmList[point][3]
        cv2.circle(img, (cx, cy), 5, (0, 0, 255), cv2.FILLED)

        print(detector.findAngle(img, 11, 23, 25))
        print(detector.findAngle(img, 23, 11, 7))

    return img


def main():
    # cap = cv2.VideoCapture(0)

    pTime = 0
    video_path = r"C:\Users\moham\PycharmProjects\AtelierComputer-Vision\videos\7 Tips For Sitting Posture (At A Desk).mp4"
    cap = cv2.VideoCapture(video_path)

    detector = poseDetector()
    while True:
        success, img = cap.read()
        img1 = img.copy()
        img1 = detector.findPose(img1)
        lmList = detector.findPosition(img, draw=True)
        if len(lmList) != 0:
            point = 11
            cx, cy = lmList[point][2], lmList[point][3]
            cv2.circle(img, (cx, cy), 5, (0, 0, 255), cv2.FILLED)
            point = 23
            cx, cy = lmList[point][2], lmList[point][3]
            cv2.circle(img, (cx, cy), 5, (0, 0, 255), cv2.FILLED)
            point = 25
            cx, cy = lmList[point][2], lmList[point][3]
            cv2.circle(img, (cx, cy), 5, (0, 0, 255), cv2.FILLED)

            point = 7
            cx, cy = lmList[point][2], lmList[point][3]
            cv2.circle(img, (cx, cy), 5, (0, 0, 255), cv2.FILLED)
            point = 9
            cx, cy = lmList[point][2], lmList[point][3]
            cv2.circle(img, (cx, cy), 5, (0, 0, 255), cv2.FILLED)
            point = 10
            cx, cy = lmList[point][2], lmList[point][3]
            cv2.circle(img, (cx, cy), 5, (0, 0, 255), cv2.FILLED)

            print(detector.findAngle(img, 11, 23, 25))
            print(detector.findAngle(img, 23, 11, 7))

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 0), 3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)


image_path = r"C:\Users\moham\PycharmProjects\AtelierComputer-Vision\Sitting Posture Correction\400-frame.jpg"
org_img = cv2.imread(image_path)
if __name__ == "__main__":
    main()

    # detector = poseDetector()
    # final_image = image_detector(org_img, detector)
    # cv2.imshow("Image", final_image)
    # cv2.waitKey(0)
