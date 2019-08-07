import abc
import datetime
from typing import List

import numpy as np

from py_motion_detector.models.bounding_box import BoundingBox


class MotionDetectionCallbackABC(abc.ABC):
    """

    """
    @abc.abstractmethod
    def on_start(self) -> None:
        pass

    @abc.abstractmethod
    def execute(self, frame: np.array, timestamp: datetime.datetime, bounding_boxes: List[BoundingBox]) -> None:
        pass

    @abc.abstractmethod
    def on_exit(self) -> None:
        pass