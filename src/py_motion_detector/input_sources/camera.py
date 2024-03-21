from typing import Iterator, Optional

import cv2
import numpy as np

from py_motion_detector.input_sources.base import FrameProviderABC


class CameraFrameProvider(FrameProviderABC):
    """
    Physical camera input source.

    Example usage:
    with CameraFrameProvider(200) as cfp:
        for img in cfp.frames():
            cv2.imshow("", img)
            cv2.waitKey(1)
    """

    def __init__(self, resize_frame: Optional[int] = None, video_capture_index: int = 0):
        self._resize_frame = resize_frame
        self._video_capture_index = video_capture_index
        self.video_capture = None

    def __enter__(self):
        self.video_capture = cv2.VideoCapture(self._video_capture_index)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.video_capture.release()
        cv2.destroyAllWindows()

    def frames(self) -> Iterator[np.array]:
        while self.video_capture.isOpened():
            frame = self.video_capture.read()
            yield self.resize_frame(frame[1])

    @property
    def resize_to(self) -> int:
        return self._resize_frame
