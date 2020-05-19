import datetime
from typing import List

import cv2
import numpy as np

from py_motion_detector.callbacks.callback_abc import MotionDetectionCallbackABC
from py_motion_detector.models.bounding_box import BoundingBox
from py_motion_detector.common.plotting import plot_bounding_boxes, plot_timestamp_to_frame


class ObjectPlotterCallback(MotionDetectionCallbackABC):
    """

    """

    def __init__(self, wait_key=1):
        self.wait_key = wait_key

    def on_start(self):
        pass

    def execute(self, frame: np.array, timestamp: datetime.datetime, bounding_boxes: List[BoundingBox]):
        frame = plot_bounding_boxes(frame, bounding_boxes)
        frame = plot_timestamp_to_frame(frame, timestamp)
        cv2.imshow("Debug Plot", frame)
        cv2.waitKey(self.wait_key)

    def on_exit(self):
        pass
