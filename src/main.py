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

options = mp.tasks.vision.FaceLandmarkerOptions(
    base_options=mp.tasks.BaseOptions(
        model_asset_path=str(MODEL_PATH)
    ),
    running_mode=mp.tasks.vision.RunningMode.IMAGE,
    num_faces=1,
)

landmarker = mp.tasks.vision.FaceLandmarker.create_from_options(options)
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    raise RuntimeError("No se pudo abrir la camara")



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

        else: 
            message = 'Sin rostro'
            color = (0, 0 , 255)
        
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
