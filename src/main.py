import cv2
import mediapipe as mp

from config import CAMERA_INDEX, MODEL_PATH, WINDOW_NAME
from drawing import (
    draw_blink_count,
    draw_expression_overlay,
    draw_face_status,
    draw_landmark_points,
)
from expressions import ExpressionTracker


def create_landmarker():
    if not MODEL_PATH.is_file():
        raise FileNotFoundError(f"No se encontro el modelo: {MODEL_PATH}")

    options = mp.tasks.vision.FaceLandmarkerOptions(
        base_options=mp.tasks.BaseOptions(
            model_asset_path=str(MODEL_PATH),
        ),
        running_mode=mp.tasks.vision.RunningMode.IMAGE,
        num_faces=1,
        output_face_blendshapes=True,
    )

    return mp.tasks.vision.FaceLandmarker.create_from_options(options)


def create_mediapipe_image(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb_frame,
    )


def main():
    tracker = ExpressionTracker()

    with create_landmarker() as landmarker:
        camera = cv2.VideoCapture(CAMERA_INDEX)

        if not camera.isOpened():
            camera.release()
            raise RuntimeError("No se pudo abrir la camara")

        try:
            while True:
                ok, frame = camera.read()

                if not ok:
                    print("No se pudo leer el fotograma")
                    break

                frame = cv2.flip(frame, 1)
                mp_image = create_mediapipe_image(frame)
                result = landmarker.detect(mp_image)
                face_detected = bool(result.face_landmarks)

                draw_face_status(frame, face_detected)

                if face_detected:
                    face = result.face_landmarks[0]
                    blendshapes = (
                        result.face_blendshapes[0]
                        if result.face_blendshapes
                        else []
                    )
                    height, width = frame.shape[:2]
                    state = tracker.update(
                        face,
                        blendshapes,
                        width,
                        height,
                    )

                    draw_landmark_points(frame, face)
                    draw_expression_overlay(frame, state)
                else:
                    tracker.reset_detection()

                draw_blink_count(frame, tracker.blink_count)
                cv2.imshow(WINDOW_NAME, frame)

                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    break
        finally:
            camera.release()
            cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
