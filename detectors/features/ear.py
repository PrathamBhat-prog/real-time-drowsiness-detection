import math


LEFT_EYE  = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]


def euclidean_distance(p1, p2):
    return math.dist(p1, p2)


def eye_aspect_ratio(eye_points):
    A = euclidean_distance(eye_points[1], eye_points[5])
    B = euclidean_distance(eye_points[2], eye_points[4])
    C = euclidean_distance(eye_points[0], eye_points[3])

    return (A + B) / (2.0 * C)


def compute_ear(landmarks, frame_width, frame_height):
    left_eye = []
    right_eye = []

    for idx in LEFT_EYE:
        lm = landmarks.landmark[idx]
        left_eye.append((int(lm.x * frame_width), int(lm.y * frame_height)))

    for idx in RIGHT_EYE:
        lm = landmarks.landmark[idx]
        right_eye.append((int(lm.x * frame_width), int(lm.y * frame_height)))

    left_ear = eye_aspect_ratio(left_eye)
    right_ear = eye_aspect_ratio(right_eye)

    return (left_ear + right_ear) / 2.0, left_eye + right_eye
