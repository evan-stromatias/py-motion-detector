import abc
from typing import List

import numpy as np

from py_motion_detector.models.bounding_box import BoundingBox


class MotionDetectionModelABC(abc.ABC):
    @abc.abstractmethod
    def next_frame(self, frame: np.asarray) -> List[BoundingBox]:
        pass
