from typing import Generator, Optional

import cv2
import numpy as np

from py_motion_detector.input_sources.base import FrameProviderABC


class VideoFileFrameProvider(FrameProviderABC):
    """
    The input source of frames is a video.

    Example usage:
        with VideoFileFrameProvider("PATH/TO/VIDEO.mp4") as vfp:
        for img in vfp.frames():
            cv2.imshow("", img)
            cv2.waitKey(1)
        cv2.destroyAllWindows()
    """

    def __init__(self, path_to_video_file: str, resize_frame: Optional[int] = None):
        self.path_to_video_file = path_to_video_file
        self._resize_frame = resize_frame

    @property
    def resize_to(self) -> int:
        return self._resize_frame

    def frames(self) -> Generator[np.array, None, None]:
        while self.video_capture.isOpened():
            ret, frame = self.video_capture.read()
            frame = frame if self._resize_frame is None else self.resize_frame(frame)
            yield frame

    def __enter__(self):
        self.video_capture = cv2.VideoCapture(self.path_to_video_file)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.video_capture.release()
        cv2.destroyAllWindows()
