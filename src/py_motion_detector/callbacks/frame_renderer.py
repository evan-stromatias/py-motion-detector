import datetime
from typing import List

import cv2
import numpy as np
import structlog

from py_motion_detector.callbacks.base import MotionDetectionCallbackABC
from py_motion_detector.common.plotting import plot_bounding_boxes, plot_timestamp_to_frame
from py_motion_detector.models.bounding_box import BoundingBox

logger = structlog.get_logger()


class FrameRendererCallback(MotionDetectionCallbackABC):
    """A callback class that renders images where motion was detected to a window"""

    def on_start(self):
        """
        Executed when the motion detection application starts and will attempt to create the directory where motion
        data will be stored.
        """
        logger.info(f"Initializing callback class '{self.name()}'.", callback=self.name())

    def execute(self, frame: np.array, timestamp: datetime.datetime, bounding_boxes: List[BoundingBox]):
        """
        Args:
            frame: The image for which motion was detected.
            timestamp: The timestamp when a motion was detected.
            bounding_boxes: A list of bounding boxes indicating the regions where motion was detected.
        """
        frame = plot_timestamp_to_frame(frame, timestamp)
        frame = plot_bounding_boxes(frame, bounding_boxes)

        cv2.imshow(f"{self.name()}", frame)
        key = cv2.waitKey(1)
        if key == 27:
            msg = f"{self.name()}: Escape key was pressed. Raising a KeyboardInterrupt exception to exit the app."
            logger.info(msg)
            raise KeyboardInterrupt(msg)

    def on_exit(self):
        logger.info(f"Shutting down callback class '{self.name()}'.", callback=self.name())
