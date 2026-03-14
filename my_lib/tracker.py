import cv2
import numpy as np
from typing import Optional, Tuple

from my_lib.constants import (MOG2_HISTORY, MOG2_VAR_THRESHOLD, MOG2_DETECT_SHADOWS,
                              MORPH_KERNEL_SIZE, MIN_CONTOUR_AREA)


class BallTracker:

    def __init__(self):
        self.fgbg = cv2.createBackgroundSubtractorMOG2(
            history=MOG2_HISTORY, # последние MOG2_HISTORY кадров, чтобы лучше понимать, что такое фон
        varThreshold=MOG2_VAR_THRESHOLD, # чувствительность
            detectShadows=MOG2_DETECT_SHADOWS
        )

        self.kernel = cv2.getStructuringElement(
            cv2.MORPH_ELLIPSE,
            MORPH_KERNEL_SIZE
        )

        self.min_area = MIN_CONTOUR_AREA # не считать шарики размером меньше MIN_CONTOUR_AREA пикселей

    def preprocess_mask(self, fgmask: np.ndarray) -> np.ndarray:
        mask = cv2.erode(fgmask, self.kernel, iterations=1)
        mask = cv2.dilate(mask, self.kernel, iterations=2)
        return mask

    def find_largest_contour(self, mask: np.ndarray) -> Optional[np.ndarray]:
        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )
        if not contours:
            return None

        largest = max(contours, key=cv2.contourArea)
        if cv2.contourArea(largest) < self.min_area:
            return None

        return largest

    def get_contour_center(self, contour: np.ndarray) -> Optional[Tuple[int, int]]:
        M = cv2.moments(contour)
        if M["m00"] == 0:
            return None

        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        return (cX, cY)

    def track(self, frame: np.ndarray) -> Optional[Tuple[int, int]]:

        # Получаем маску переднего плана
        fgmask = self.fgbg.apply(frame)

        fgmask = self.preprocess_mask(fgmask)

        contour = self.find_largest_contour(fgmask)
        if contour is None:
            return None

        # Вычисляем центр
        center = self.get_contour_center(contour)
        return center