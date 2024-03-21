import abc
from typing import Iterator

import cv2
import numpy as np


class FrameProviderABC(abc.ABC):
    """All input sources are context managers."""

    def __enter__(self):
        return self

    @abc.abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @abc.abstractmethod
    def frames(self) -> Iterator[np.array]:
        """Generator that yields the next frame as numpy array."""

    @property
    @abc.abstractmethod
    def resize_to(self) -> int:
        """Integer value to resize the frame."""

    def resize_frame(self, frame: np.array) -> np.array:
        """Resize the current frame based on the resize_to property."""
        frame = cv2.resize(frame, (self.resize_to, self.resize_to)) if self.resize_to and frame is not None else frame
        return frame
