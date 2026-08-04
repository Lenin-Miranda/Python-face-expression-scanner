import cv2

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    raise RuntimeError("No se pudo abrir la camara")



try: 
    while True:
        ok, frame = camera.read()

        height, width, channels = frame.shape

        frame = cv2.flip(frame, 1)

        cv2.putText(
            frame,
            f"Resolucion: {width} x {height}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
        )

        if not ok:
            print("No se pudo leer el fotograma")
            break

        cv2.imshow("Mi camara", frame)

        key = cv2.waitKey(1) & 0xFF


        if key == ord("q"):
            break
finally:
    camera.release()
    cv2.destroyAllWindows()
