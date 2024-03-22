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

    def __init__(
        self,
        min_area: int = 1000,
        delta_threshold: int = 10,
        g_kernel: tuple[int, int] = (21, 21),
        acc_weight: float = 0.3,
        dil_iters: int = 10,
    ):
        """

        Args:
            min_area: Used as a threshold to get the bounding boxes from the image contours. Any value below this area
                will not produce a bounding box.
            delta_threshold: Used as a threshold value for OpenCV's `cv2.threshold` function.
            g_kernel: Size of the gaussian kernel used to blur the input image to remove noise.
            acc_weight: Weight of the input image. It regulates the update speed (how fast the accumulator “forgets”
                earlier images).
            dil_iters: Number of iterations to run the OpenCV's dilate function before extracting the bounding boxes.
        """
        self.min_area = min_area
        self.delta_threshold = delta_threshold

        self._weighted_average_image = None
        self.counter = 0

        self._gkernel = g_kernel
        self._weight = acc_weight
        self._dil_iter = dil_iters
        logger.info(f"Motion detection model '{self.name()}' has been initialized.")

    def next_frame(self, frame: np.array) -> List[BoundingBox]:

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, self._gkernel, 0)

        if self._weighted_average_image is None:
            logger.info(f"{self.name()}: Starting background image.")
            self._weighted_average_image = gray.copy().astype("float")
            return []

        # update the running average
        cv2.accumulateWeighted(gray, self._weighted_average_image, self._weight)
        frame_delta = cv2.absdiff(gray, cv2.convertScaleAbs(self._weighted_average_image))

        ret, thresh = cv2.threshold(frame_delta, self.delta_threshold, 255, cv2.THRESH_BINARY)
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
