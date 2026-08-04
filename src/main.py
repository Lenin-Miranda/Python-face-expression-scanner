from pathlib import Path

import cv2
import mediapipe as mp


MODEL_PATH = (
    Path(__file__).resolve().parent.parent
    / "models"
    / "face_landmarker.task"
)

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
