from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = PROJECT_ROOT / "models" / "face_landmarker.task"

CAMERA_INDEX = 0
WINDOW_NAME = "Mi camara"

MOUTH_OPEN_THRESHOLD = 0.08
EYE_CLOSED_THRESHOLD = 0.18
SMILE_THRESHOLD = 0.45
MIN_CLOSED_FRAMES = 2
SMOOTHING_WINDOW = 3

HIGHLIGHTED_POINTS = {
    # Boca: superior, inferior, izquierda y derecha.
    13: (255, 0, 255),
    14: (255, 0, 255),
    61: (255, 0, 255),
    291: (255, 0, 255),
    # Ojo izquierdo de la persona en la imagen reflejada.
    33: (255, 255, 0),
    133: (255, 255, 0),
    159: (255, 255, 0),
    145: (255, 255, 0),
    # Ojo derecho de la persona en la imagen reflejada.
    362: (0, 165, 255),
    263: (0, 165, 255),
    386: (0, 165, 255),
    374: (0, 165, 255),
}

