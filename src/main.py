import cv2

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    raise RuntimeError("No se pudo abrir la camara")

try: 
    while True:
        ok, frame = camera.read()

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
