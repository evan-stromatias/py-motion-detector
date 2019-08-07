from typing import List
import logging

import cv2
import imutils
import numpy as np

from py_motion_detector.models.bounding_box import BoundingBox
from py_motion_detector.models.motion_detection.motion_detection_model_abc import MotionDetectionModelABC

logger = logging.getLogger(__name__)


class MotionDetectionWeightedAverage(MotionDetectionModelABC):
    def __init__(self, min_area=5000, delta_threshold=5):
        self.min_area = min_area
        self.delta_threshold = delta_threshold

        self.weighted_average = None
        self.counter = 0
        logger.info('Motion detection model has been initialized')

    def next_frame(self, frame: np.array) -> List[BoundingBox]:

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if self.weighted_average is None:
            logger.info('Starting background image')
            self.weighted_average = gray.copy().astype("float")
            return []

        cv2.accumulateWeighted(gray, self.weighted_average, 0.5)
        frame_delta = cv2.absdiff(gray, cv2.convertScaleAbs(self.weighted_average))

        thresh = cv2.threshold(frame_delta, self.delta_threshold, 255,
                               cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)

        contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
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
