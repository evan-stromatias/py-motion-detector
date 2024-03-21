from typing import List

import cv2
import numpy as np
import structlog

from py_motion_detector.models.bounding_box import BoundingBox
from py_motion_detector.models.motion_detection.base import MotionDetectionModelABC

logger = structlog.get_logger()


class MotionDetectionWeightedAverage(MotionDetectionModelABC):
    """
    A basic motion detection algorithm using a stationary input source and OpenCV`AccumulatedWeighted` which updates a
    running average.
    """

    def __init__(self, min_area: int = 5000, delta_threshold: int = 5):
        self.min_area = min_area
        self.delta_threshold = delta_threshold

        self.weighted_average = None
        self.counter = 0

        self._gkernel = (21, 21)
        self._weight = 0.5
        self._dil_iter = 2
        logger.info(f"Motion detection model '{self.name()}' has been initialized.")

    def next_frame(self, frame: np.array) -> List[BoundingBox]:

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, self._gkernel, 0)

        if self.weighted_average is None:
            logger.info(f"{self.name()}: Starting background image.")
            self.weighted_average = gray.copy().astype("float")
            return []

        cv2.accumulateWeighted(gray, self.weighted_average, self._weight)
        frame_delta = cv2.absdiff(gray, cv2.convertScaleAbs(self.weighted_average))

        thresh = cv2.threshold(frame_delta, self.delta_threshold, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=self._dil_iter)

        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return self.bounding_boxes_from_contours(contours)

    def bounding_boxes_from_contours(self, cv2_contours) -> List[BoundingBox]:
        bounding_boxes = []

        for c in cv2_contours:
            if cv2.contourArea(c) < self.min_area:
                continue

            (x, y, w, h) = cv2.boundingRect(c)
            bounding_box = BoundingBox(top=y, left=x, bottom=y + h, right=x + w)
            bounding_boxes.append(bounding_box)
        return bounding_boxes
