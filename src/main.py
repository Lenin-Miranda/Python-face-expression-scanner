from pathlib import Path
from collections import deque
from pathlib import Path

import cv2
import mediapipe as mp



MODEL_PATH = (
    Path(__file__).resolve().parent.parent
    / "models"
    / "face_landmarker.task"
)

HIGHLIGHTED_POINTS = {
    # Boca: superior, inferior, izquierda y derecha
    13: (255, 0, 255),
    14: (255, 0, 255),
    61: (255, 0, 255),
    291: (255, 0, 255),

    # Ojo derecho de la persona
    33: (255, 255, 0),
    133: (255, 255, 0),
    159: (255, 255, 0),
    145: (255, 255, 0),

    # Ojo izquierdo de la persona
    362: (0, 165, 255),
    263: (0, 165, 255),
    386: (0, 165, 255),
    374: (0, 165, 255),
}

MOUTH_OPEN_THRESHOLD = 0.08
EYE_CLOSED_THRESHOLD = 0.18
MIN_CLOSED_FRAMES = 2
SMOORHING_WINDOW = 3

def pixel_distance(point_a, point_b, width, height):
    delta_x = (point_a.x - point_b.x) * width
    delta_y = (point_a.y - point_b.y) * height

    return (delta_x ** 2 + delta_y ** 2) ** 0.5

options = mp.tasks.vision.FaceLandmarkerOptions(
    base_options=mp.tasks.BaseOptions(
        model_asset_path=str(MODEL_PATH)
    ),
    running_mode=mp.tasks.vision.RunningMode.IMAGE,
    num_faces=1,
)

def opening_ratio(
        face,
        top_index,
        bottom_index,
        left_index,
        right_index,
        width,
        height,
):
    opening = pixel_distance(
        face[top_index],
        face[bottom_index],
        width,
        height,
    )

    feature_width = pixel_distance(
        face[left_index],
        face[right_index],
        width,
        height,
    )

    if feature_width == 0:
        return 0.0

    return opening / feature_width

landmarker = mp.tasks.vision.FaceLandmarker.create_from_options(options)
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    raise RuntimeError("No se pudo abrir la camara")


blink_count = 0
closed_frame_count = 0
mouth_ratio_history = deque(maxlen=SMOORHING_WINDOW)
right_eye_ratio_history = deque(maxlen=SMOORHING_WINDOW)
left_eye_ratio_history = deque(maxlen=SMOORHING_WINDOW)



try: 
    while True:
        ok, frame = camera.read()

        if not ok:
            print("No se pudo leer el fotograma")
            break

        height, width, channels = frame.shape
        
        frame = cv2.flip(frame, 1)

        rgb_frame=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame,
        )

        result = landmarker.detect(mp_image)

        face_detected = bool(result.face_landmarks)

        if face_detected:
            message = "Rostro detectado"
            color = (0, 255, 0)

            face = result.face_landmarks[0]
            mouth_opening = opening_ratio(
                face,
                13,
                14,
                61,
                291,
                width,
                height,
            )

            mouth_width = pixel_distance(
                face[61],
                face[291],
                width,
                height,
            )

            mouth_ratio = opening_ratio(
                face,
                13,
                14,
                61,
                291,
                width,
                height,
            )


            left_eye_ratio = opening_ratio(
                face,
                159,
                145,
                33,
                133,
                width,
                height,
            )

            right_eye_ratio = opening_ratio(
                face,
                386,
                374,
                362,
                263,
                width,
                height,
            )

            mouth_ratio_history.append(mouth_ratio)
            right_eye_ratio_history.append(right_eye_ratio)
            left_eye_ratio_history.append(left_eye_ratio)

            mouth_ratio = sum(mouth_ratio_history) / len(mouth_ratio_history)

            right_eye_ratio = (
                sum(right_eye_ratio_history) / len(right_eye_ratio_history)
            )

            left_eye_ratio = (
                sum(left_eye_ratio_history)
                / len(left_eye_ratio_history)
            )

            right_eye_closed = right_eye_ratio < EYE_CLOSED_THRESHOLD
            left_eye_closed = left_eye_ratio < EYE_CLOSED_THRESHOLD

            both_eyes_closed = right_eye_closed and left_eye_closed

            if both_eyes_closed:
                closed_frame_count += 1
            else:
                if closed_frame_count >= MIN_CLOSED_FRAMES:
                    blink_count += 1

                closed_frame_count = 0

            if mouth_ratio > MOUTH_OPEN_THRESHOLD:
                mouth_message = f'Boca abierta: {mouth_ratio:.2f}'
                mouth_color = (0, 255, 255)

            else:
                mouth_message = f'Boca cerrada: {mouth_ratio:.2f}'
                mouth_color = (255, 255, 255)

            if right_eye_closed and left_eye_closed:
                eye_message = "Ambos ojos cerrados"
                eye_color = (0, 0, 255)
            elif right_eye_closed:
                eye_message = "Ojo derecho cerrado"
                eye_color = (0,255,255)
            elif left_eye_closed:
                eye_message = 'Ojo izquierdo cerrado'
                eye_color = (0, 255,255)
            else:
                eye_message = 'Ojos abiertos'
                eye_color = (0, 255, 0)

            for index, point_color in HIGHLIGHTED_POINTS.items():
                landmark = face[index]

                x = int(landmark.x * width)
                y = int(landmark.y * height)

                cv2.circle(
                    frame,
                    (x, y),
                    5,
                    point_color,
                    -1,
                )

                cv2.putText(
                    frame,
                    str(index),
                    (x + 5, y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.4,
                    point_color,
                    1,
                )

            right_history_text = ', '.join(
                f'{value:.2f}'
                for value in right_eye_ratio_history
            )

            left_history_text = ', '.join(
                f'{value:.2f}'
                for value in left_eye_ratio_history
            )

            cv2.putText(
                    frame,
                    mouth_message,
                    (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    mouth_color,
                    2,
                )

            cv2.putText(
                    frame,
                    (
                        f'{eye_message}'
                        f"D: {right_eye_ratio: .2f}"
                        f"I: {left_eye_ratio: .2f}"
                    ),
                    (20,120),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    eye_color,
                    2,
                )

            cv2.putText(
                    frame,
                    f'Parpadeos: {blink_count}',
                    (20, 160),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (255, 255, 255),
                    2,
                )

            cv2.putText(
                frame,
                f'Hist D: [{right_history_text}]',
                (20, 200),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (200, 200, 200),
                1,
            )

            cv2.putText(
                frame,
                f'Hist I: [{left_history_text}]',
                (20, 230),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (200,200,200),
                1,
            )

        else: 
            message = 'Sin rostro'
            color = (0, 0 , 255)
            closed_frame_count = 0

            mouth_ratio_history.clear()
            right_eye_ratio_history.clear()
            left_eye_ratio_history.clear()
        
        cv2.putText(
                    frame,
                    message,
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    color,
                    2,
                )
        
            
        cv2.imshow("Mi camara", frame)

        key = cv2.waitKey(1) & 0xFF


        if key == ord("q"):
            break
finally:
    landmarker.close()
    camera.release()
    cv2.destroyAllWindows()
