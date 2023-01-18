import json
import cv2

# import location of 33 pose landmarks / the output of Mediapipe
from model.poseDetector import poseDetector

with open('data/landmarks-data/landmarks-labels.json', 'r') as fp:
    landmarks_data = json.load(fp)


def draw_circles(img, points, colour=(0, 0, 255)):
    if len(points) == 0:
        return "ERROR DRAWING CIRCLES"
    else:
        for point in points:
            _, _, cx, cy = point
            cv2.circle(img, (cx, cy), 5, colour, cv2.FILLED)
        return img


def draw_lines(img, points, colour=(0, 0, 255)):
    if len(points) == 0 or len(points) % 2 == 0:
        return "ERROR DRAWING LINES"
    else:
        _, _, x1, y1 = points[0]
        _, _, x2, y2 = points[1]
        _, _, x3, y3 = points[2]
        cv2.line(img, (x1, y1), (x2, y2), colour, 2)
        cv2.line(img, (x3, y3), (x2, y2), colour, 2)
        return img


def alignment(detector, desired_angle, tolerance, pt1_id, pt2_id, pt3_id):
    """
    :param detector: The detector to use that contains a function to calculate the angle between 3points
    :param desired_angle: The angle that is perfect between these 3 points
    :param tolerance: Eligibility to be around the desired angle
    :param pt1_id: Point1 ID
    :param pt2_id: Point2 ID
    :param pt3_id: Point3 ID
    :return: Whether the calculated angle respects the conditions
    """
    angle = detector.findAngle(pt1_id, pt2_id, pt3_id)
    return desired_angle - tolerance <= abs(angle) <= desired_angle + tolerance


def process(detector, org_img, imList, points, desired_angle, tolerance):
    angle = alignment(detector, desired_angle, tolerance, landmarks_data[points[0]], landmarks_data[points[1]],
                      landmarks_data[points[2]])
    # ---------  draw the lines and circles ------------
    if angle:
        colour = (0, 255, 0)
    else:
        colour = (0, 0, 255)
    final_image = draw_lines(org_img, [imList[landmarks_data[elt]] for elt in points], colour)
    final_image = draw_circles(final_image, [imList[landmarks_data[elt]] for elt in points], colour)
    return final_image, angle


def main():
    image_path = r"C:\Users\moham\PycharmProjects\AtelierComputer-Vision\Sitting Posture Correction\400-frame.jpg"
    org_img = cv2.imread(image_path)
    detector = poseDetector()
    imList = detector.findLandmarks(org_img)

    # # ---------  alignment of 3 points of SIDE TOP------------
    # points = ["right_hip", "right_shoulder", "right_ear"]
    #
    # desired_angle = 180
    # tolerance = 5
    #
    # angle = alignment(detector, desired_angle, tolerance, landmarks_data[points[0]], landmarks_data[points[1]],
    #                   landmarks_data[points[2]])
    # print(angle)
    # # ---------  draw the lines and circles ------------
    # if angle:
    #     colour = (0, 255, 0)
    # else:
    #     colour = (0, 0, 255)
    # final_image = draw_lines(org_img, [imList[landmarks_data[elt]] for elt in points], colour)
    # final_image = draw_circles(final_image, [imList[landmarks_data[elt]] for elt in points], colour)
    # # --------------------------------------------------
    #
    # # ---------  alignement of 3 points SIDE MIDDLE------------
    # points = ["right_shoulder", "right_elbow", "right_wrist"]
    #
    # desired_angle = 90
    # tolerance = 5
    #
    # angle = alignment(detector, desired_angle, tolerance, landmarks_data[points[0]], landmarks_data[points[1]],
    #                   landmarks_data[points[2]])
    # print(angle)
    # # ---------  draw the lines and circles ------------
    # if angle:
    #     colour = (0, 255, 0)
    # else:
    #     colour = (0, 0, 255)
    # final_image = draw_lines(final_image, [imList[landmarks_data[elt]] for elt in points], colour)
    # final_image = draw_circles(final_image, [imList[landmarks_data[elt]] for elt in points], colour)
    # # --------------------------------------------------
    #
    # # ---------  alignement of 3 points SIDE BOTTOM------------
    # points = ["right_ankle", "right_knee", "right_hip"]
    #
    # desired_angle = 90
    # tolerance = 5
    #
    # angle = alignment(detector, desired_angle, tolerance, landmarks_data[points[0]], landmarks_data[points[1]],
    #                   landmarks_data[points[2]])
    # print(angle)
    # # ---------  draw the lines and circles ------------
    # if angle:
    #     colour = (0, 255, 0)
    # else:
    #     colour = (0, 0, 255)
    # final_image = draw_lines(final_image, [imList[landmarks_data[elt]] for elt in points], colour)
    # final_image = draw_circles(final_image, [imList[landmarks_data[elt]] for elt in points], colour)
    # # --------------------------------------------------

    points_TOP = ["right_hip", "right_shoulder", "right_ear"]
    final_image = process(detector, org_img, imList, points_TOP, 180, 15)

    points_MIDDLE = ["right_shoulder", "right_elbow", "right_wrist"]
    final_image = process(detector, final_image, imList, points_MIDDLE, 90, 10)

    points_BOTTOM = ["right_ankle", "right_knee", "right_hip"]
    final_image = process(detector, final_image, imList, points_BOTTOM, 90, 10)

    cv2.imshow("Image", final_image)
    cv2.waitKey(0)


def main2():
    input_video_path = r"C:\Users\moham\PycharmProjects\AtelierComputer-Vision\videos\7 Tips For Sitting Posture (At A Desk).mp4"
    cap = cv2.VideoCapture(input_video_path)
    detector = poseDetector()
    side = "left"
    points_TOP = [f"{side}_hip", f"{side}_shoulder", f"{side}_ear"]
    points_MIDDLE = [f"{side}_shoulder", f"{side}_elbow", f"{side}_wrist"]
    points_BOTTOM = [f"{side}_ankle", f"{side}_knee", f"{side}_hip"]

    while (cap.isOpened()):
        ret, img = cap.read()

        imList = detector.findLandmarks(img)

        final_image, _ = process(detector, img, imList, points_TOP, 180, 15)
        final_image, _ = process(detector, final_image, imList, points_MIDDLE, 90, 10)
        final_image, _ = process(detector, final_image, imList, points_BOTTOM, 90, 10)

        cv2.imshow("Image", final_image)
        cv2.waitKey(1)


def video():
    cap = cv2.VideoCapture(0)
    detector = poseDetector()
    side = "right"
    points_TOP = [f"{side}_hip", f"{side}_shoulder", f"{side}_ear"]
    points_MIDDLE = [f"{side}_shoulder", f"{side}_elbow", f"{side}_wrist"]
    points_BOTTOM = [f"{side}_ankle", f"{side}_knee", f"{side}_hip"]
    while True:
        success, img = cap.read()
        try:
            imList = detector.findLandmarks(img)
            final_image, _ = process(detector, img, imList, points_TOP, 180, 15)
            final_image, _ = process(detector, final_image, imList, points_MIDDLE, 90, 10)
            final_image, _ = process(detector, final_image, imList, points_BOTTOM, 90, 10)

            cv2.imshow("Image", final_image)
        except:
            print("error")
            cv2.imshow("Image", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    # Destroy all the windows
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main2()
    # video()
