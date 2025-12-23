def estimate_attention(landmarks):
    """
    Very simple yaw-based attention estimation.
    """
    nose = landmarks.landmark[1]
    left_eye = landmarks.landmark[33]
    right_eye = landmarks.landmark[263]

    nose_x = nose.x
    eye_center_x = (left_eye.x + right_eye.x) / 2.0

    if abs(nose_x - eye_center_x) > 0.03:
        return "LOOKING_AWAY"
    return "ATTENTIVE"
