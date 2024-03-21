import abc
from typing import List

import numpy as np

from py_motion_detector.models.bounding_box import BoundingBox


class MotionDetectionModelABC(abc.ABC):
    """The base class all motion detection algorithms need to implement."""

    @abc.abstractmethod
    def next_frame(self, frame: np.asarray) -> List[BoundingBox]:
        """
        Returns a list of bounding boxes if a motion has been detected. If no motion detected then it returns an empty
        list.
        """

    @classmethod
    def name(cls) -> str:
        return cls.__name__
