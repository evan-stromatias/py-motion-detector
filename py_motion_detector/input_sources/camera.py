from typing import Optional

import numpy as np
import cv2

from py_motion_detector.input_sources.frame_provider_abc import FrameProviderABC


class CameraFrameProvider(FrameProviderABC):
    """
    The source of frames is the camera
    """

    def __init__(self, resize_frame: Optional[int] = None, video_capture_index: int = 0):
        self._resize_frame = resize_frame
        self.video_capture = cv2.VideoCapture(video_capture_index)

    @property
    def has_finished(self) -> bool:
        return not self.video_capture.isOpened()

    @property
    def resize_to(self) -> int:
        return self._resize_frame

    def next_frame(self) -> np.array:
        if self.video_capture.isOpened():
            frame = self.video_capture.read()
            return self.resize_frame(frame[1])

    def on_exit(self):
        self.video_capture.release()
        cv2.destroyAllWindows()
