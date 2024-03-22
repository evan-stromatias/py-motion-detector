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
        This method is called by the `MotionDetectionApplication` for every input frame.

        Args:
            frame: The current input image.
            timestamp: The current timestamp.
            bounding_boxes: A list of bounding boxes indicating the regions where motion was detected. If no motion was
                detected then this will be an empty list.
        """

    @abc.abstractmethod
    def on_exit(self) -> None:
        """Executed when the motion detection application ends."""

    @classmethod
    def name(cls) -> str:
        return cls.__name__
