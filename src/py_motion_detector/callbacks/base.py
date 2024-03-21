import abc
import datetime
from typing import List

import numpy as np

from py_motion_detector.models.bounding_box import BoundingBox


class MotionDetectionCallbackABC(abc.ABC):
    """The base callback class used to respond to motion detected events."""

    @abc.abstractmethod
    def on_start(self) -> None:
        """Executed when the motion detection application starts."""

    @abc.abstractmethod
    def execute(self, frame: np.array, timestamp: datetime.datetime, bounding_boxes: List[BoundingBox]) -> None:
        """
        Executed when a motion has been detected.

        Args:
            frame: The image for which motion was detected.
            timestamp: The timestamp when a motion was detected.
            bounding_boxes: A list of bounding boxes indicating the regions where motion was detected.
        """

    @abc.abstractmethod
    def on_exit(self) -> None:
        """Executed when the motion detection application ends."""

    @classmethod
    def name(cls) -> str:
        return cls.__name__
