from typing import Iterator, Optional

import numpy as np

from py_motion_detector.input_sources.base import FrameProviderABC


class DummyFrameProvider(FrameProviderABC):
    """
    A dummy input source Used for the unit tests. Yields the same numpy array specified by the repeat property.
    """

    def next_frame(self) -> np.array:
        pass

    def __init__(self, dummy_frame: np.array, repeat: int = 1, resize_frame: Optional[int] = None):
        self.dummy_frames = [dummy_frame] * repeat
        self._resize_frame = resize_frame

    @property
    def resize_to(self) -> int:
        return self._resize_frame

    def frames(self) -> Iterator[np.array]:
        for img in self.dummy_frames:
            yield self.resize_frame(img)

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
