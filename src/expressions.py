from collections import deque
from dataclasses import dataclass

from config import (
    EYE_CLOSED_THRESHOLD,
    MIN_CLOSED_FRAMES,
    MOUTH_OPEN_THRESHOLD,
    SMILE_THRESHOLD,
    SMOOTHING_WINDOW,
)
from geometry import opening_ratio


@dataclass(frozen=True)
class ExpressionState:
    mouth_ratio: float
    mouth_open: bool
    right_eye_ratio: float
    left_eye_ratio: float
    right_eye_closed: bool
    left_eye_closed: bool
    smile_score: float
    smiling: bool
    blink_count: int
    right_eye_history: tuple[float, ...]
    left_eye_history: tuple[float, ...]


class ExpressionTracker:
    """Analiza expresiones visibles y conserva estado entre fotogramas."""

    def __init__(self):
        self._blink_count = 0
        self._closed_frame_count = 0
        self._mouth_history = deque(maxlen=SMOOTHING_WINDOW)
        self._right_eye_history = deque(maxlen=SMOOTHING_WINDOW)
        self._left_eye_history = deque(maxlen=SMOOTHING_WINDOW)

    @property
    def blink_count(self):
        return self._blink_count

    def reset_detection(self):
        """Descarta una secuencia incompleta cuando el rostro desaparece."""
        self._closed_frame_count = 0
        self._mouth_history.clear()
        self._right_eye_history.clear()
        self._left_eye_history.clear()

    def update(self, face, blendshapes, width, height):
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

        self._mouth_history.append(mouth_ratio)
        self._right_eye_history.append(right_eye_ratio)
        self._left_eye_history.append(left_eye_ratio)

        mouth_ratio = self._average(self._mouth_history)
        right_eye_ratio = self._average(self._right_eye_history)
        left_eye_ratio = self._average(self._left_eye_history)

        right_eye_closed = right_eye_ratio < EYE_CLOSED_THRESHOLD
        left_eye_closed = left_eye_ratio < EYE_CLOSED_THRESHOLD
        self._update_blink_count(right_eye_closed and left_eye_closed)

        blendshape_scores = {
            category.category_name: category.score
            for category in blendshapes
        }
        smile_left = blendshape_scores.get("mouthSmileLeft", 0.0)
        smile_right = blendshape_scores.get("mouthSmileRight", 0.0)
        smile_score = (smile_left + smile_right) / 2

        return ExpressionState(
            mouth_ratio=mouth_ratio,
            mouth_open=mouth_ratio > MOUTH_OPEN_THRESHOLD,
            right_eye_ratio=right_eye_ratio,
            left_eye_ratio=left_eye_ratio,
            right_eye_closed=right_eye_closed,
            left_eye_closed=left_eye_closed,
            smile_score=smile_score,
            smiling=smile_score > SMILE_THRESHOLD,
            blink_count=self._blink_count,
            right_eye_history=tuple(self._right_eye_history),
            left_eye_history=tuple(self._left_eye_history),
        )

    def _update_blink_count(self, both_eyes_closed):
        if both_eyes_closed:
            self._closed_frame_count += 1
            return

        if self._closed_frame_count >= MIN_CLOSED_FRAMES:
            self._blink_count += 1

        self._closed_frame_count = 0

    @staticmethod
    def _average(values):
        return sum(values) / len(values)

