from typing import Optional, Callable
from pathlib import Path

import numpy as np
import cv2

from py_motion_detector.input_sources.frame_provider_abc import FrameProviderABC


class ImageFilesFrameProvider(FrameProviderABC):
    """
    The source of frames is a directory of images

    Example usage:

    with ImageFilesFrameProvider(PATH/TO/DIR/WITH/IMAGES, "*.jpg") as ifp:
    for img in ifp.frames():
        cv2.imshow("", img)
        cv2.waitKey(1)
    cv2.destroyAllWindows()
    """

    def next_frame(self) -> np.array:
        pass

    def __init__(self, path_to_dir: str, files_ending_with: str = ".jpg", resize_frame: Optional[int] = None,
                 sorting_function: Callable = None):
        self.sorting_function = sorting_function
        self.path_to_dir = path_to_dir
        self._resize_frame = resize_frame
        self.files_ending_with = files_ending_with

        self.image_files = self._load_files()

    def _load_files(self):
        path = Path(self.path_to_dir).glob(self.files_ending_with)
        files = [str(x) for x in path if x.is_file()]
        if self.sorting_function is None:
            files = sorted(files)
        else:
            pass
        return files

    @property
    def resize_to(self) -> int:
        return self._resize_frame

    def frames(self) -> np.array:
        for img_p in self.image_files:
            img = cv2.imread(img_p)
            yield self.resize_frame(img)
