import abc
from typing import Generator

import cv2
import numpy as np


class FrameProviderABC(abc.ABC):

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @abc.abstractmethod
    def frames(self) -> Generator[np.array, None, None]:
        """
        Generator that yields the next frame as numpy array
        """
        pass

    @property
    @abc.abstractmethod
    def resize_to(self) -> int:
        """
        :return: Integer value to resize the frame
        """

    def resize_frame(self, frame: np.array) -> np.array:
        """
        Resize the current frame based on the resize_to property.

        TODO: Keep aspect ratio
        """
        frame = cv2.resize(frame, (self.resize_to, self.resize_to)) \
            if self.resize_to and frame is not None \
            else frame
        return frame
