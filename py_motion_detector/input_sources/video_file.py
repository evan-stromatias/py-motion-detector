from typing import Optional

import numpy as np
import cv2

from py_motion_detector.input_sources.frame_provider_abc import FrameProviderABC


class VideoFileFrameProvider(FrameProviderABC):
    """
    The source of frames is a video
    """

    def __init__(self, path_to_video_file: str, resize_frame: Optional[int] = None):
        self.path_to_vide_file = path_to_video_file
        self._resize_frame = resize_frame
        self.video_capture = cv2.VideoCapture(path_to_video_file)

    @property
    def resize_to(self) -> int:
        return self._resize_frame

    @property
    def has_finished(self) -> bool:
        return self.frame_i == self.length

    @property
    def length(self) -> int:
        return int(self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

    @property
    def frame_i(self) -> int:
        return int(self.video_capture.get(cv2.CAP_PROP_POS_FRAMES))

    def next_frame(self) -> np.array:
        if self.video_capture.isOpened():
            ret, frame = self.video_capture.read()
            return self.resize_frame(frame)

    def on_exit(self):
        self.video_capture.release()
        cv2.destroyAllWindows()
