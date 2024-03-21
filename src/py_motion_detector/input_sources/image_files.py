from pathlib import Path
from typing import Callable, Optional

import cv2
import numpy as np

from py_motion_detector.input_sources.base import FrameProviderABC


class ImageFilesFrameProvider(FrameProviderABC):
    """
    The input source is a directory of images.

    Example usage:

    with ImageFilesFrameProvider(PATH/TO/DIR/WITH/IMAGES, "*.jpg") as ifp:
    for img in ifp.frames():
        cv2.imshow("", img)
        cv2.waitKey(1)
    cv2.destroyAllWindows()
    """

    def __init__(
        self,
        path_to_dir: Path,
        files_ending_with: str = ".jpg",
        resize_frame: Optional[int] = None,
        sorting_function: Callable = None,
    ):
        self.sorting_function = sorting_function
        self.path_to_dir = path_to_dir
        self._resize_frame = resize_frame
        self.files_ending_with = files_ending_with

        self.image_files = self._load_files()

    def next_frame(self) -> np.array:
        pass

    def _load_files(self):
        path = self.path_to_dir.glob(self.files_ending_with)
        files = [str(x) for x in path if x.is_file()]
        return sorted(files) if self.sorting_function is None else files

    @property
    def resize_to(self) -> int:
        return self._resize_frame

    def frames(self) -> np.array:
        for img_p in self.image_files:
            img = cv2.imread(img_p)
            yield self.resize_frame(img)

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
