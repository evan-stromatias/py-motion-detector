from pathlib import Path
from typing import Iterator

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

    def __init__(self, path_to_video_file: Path, resize_frame: int | None = None):
        self.path_to_video_file = path_to_video_file
        self._resize_frame = resize_frame  # TODO fix

    @property
    def resize_to(self) -> int | None:
        return self._resize_frame

    def frames(self) -> Iterator[np.array]:
        while self.video_capture.isOpened():
            ret, frame = self.video_capture.read()

            if not ret:
                return

            frame = frame if self._resize_frame is None else self.resize_frame(frame)
            yield frame

    def __enter__(self):
        if not self.path_to_video_file.is_file():
            raise FileNotFoundError(f"The video file '{self.path_to_video_file}' does not exist!")
        self.video_capture = cv2.VideoCapture(str(self.path_to_video_file))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.video_capture.release()
        cv2.destroyAllWindows()
