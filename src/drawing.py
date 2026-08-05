import cv2

from config import HIGHLIGHTED_POINTS


WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
YELLOW = (0, 255, 255)
RED = (0, 0, 255)


def draw_face_status(frame, face_detected):
    message = "Rostro detectado" if face_detected else "Sin rostro"
    color = GREEN if face_detected else RED
    _put_text(frame, message, (20, 40), 1, color)


def draw_landmark_points(frame, face):
    height, width = frame.shape[:2]

    for index, point_color in HIGHLIGHTED_POINTS.items():
        landmark = face[index]
        x = int(landmark.x * width)
        y = int(landmark.y * height)

        cv2.circle(frame, (x, y), 5, point_color, -1)
        _put_text(
            frame,
            str(index),
            (x + 5, y - 5),
            0.4,
            point_color,
            thickness=1,
        )


def draw_expression_overlay(frame, state):
    mouth_status = "abierta" if state.mouth_open else "cerrada"
    mouth_color = YELLOW if state.mouth_open else WHITE
    _put_text(
        frame,
        f"Boca {mouth_status}: {state.mouth_ratio:.2f}",
        (20, 80),
        0.8,
        mouth_color,
    )

    eye_message, eye_color = _eye_status(state)
    _put_text(
        frame,
        (
            f"{eye_message} "
            f"D: {state.right_eye_ratio:.2f} "
            f"I: {state.left_eye_ratio:.2f}"
        ),
        (20, 120),
        0.7,
        eye_color,
    )

    right_history = ", ".join(
        f"{value:.2f}" for value in state.right_eye_history
    )
    left_history = ", ".join(
        f"{value:.2f}" for value in state.left_eye_history
    )
    _put_text(frame, f"Hist D: [{right_history}]", (20, 200), 0.55, GRAY, 1)
    _put_text(frame, f"Hist I: [{left_history}]", (20, 230), 0.55, GRAY, 1)

    smile_status = "Sonrisa visible" if state.smiling else "Sin sonrisa"
    smile_color = YELLOW if state.smiling else WHITE
    _put_text(
        frame,
        f"{smile_status}: {state.smile_score:.2f}",
        (20, 270),
        0.7,
        smile_color,
    )


def draw_blink_count(frame, blink_count):
    _put_text(frame, f"Parpadeos: {blink_count}", (20, 160), 0.8, WHITE)


def _eye_status(state):
    if state.right_eye_closed and state.left_eye_closed:
        return "Ambos ojos cerrados", RED
    if state.right_eye_closed:
        return "Ojo derecho cerrado", YELLOW
    if state.left_eye_closed:
        return "Ojo izquierdo cerrado", YELLOW
    return "Ojos abiertos", GREEN


def _put_text(frame, text, position, scale, color, thickness=2):
    cv2.putText(
        frame,
        text,
        position,
        cv2.FONT_HERSHEY_SIMPLEX,
        scale,
        color,
        thickness,
    )

