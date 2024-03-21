import json
import sys
from itertools import cycle
from pathlib import Path

import cv2

from py_motion_detector.common.plotting import plot_bounding_boxes
from py_motion_detector.models.bounding_box import BoundingBox


def logged_data_gen(directory: Path, img_ending="*.jpg", loop_forever: bool = False):
    """Helper function that yields an image with its bounding boxes. Used by the data player."""
    image_paths = directory.glob(img_ending)
    images_sorted = sorted(image_paths)
    images = cycle(images_sorted) if loop_forever else images_sorted
    for img_p in images:
        img = cv2.imread(f"{img_p}")
        json_data = []
        json_file_name = Path(img_p).name.split(".")[0]
        json_p = directory / f"{json_file_name}.json"
        try:
            with open(json_p) as f:
                json_data = json.load(f)
        except FileNotFoundError:
            print(f"Bounding boxes for '{json_file_name}' were not found, skipping...")
        bounding_boxes = [BoundingBox.from_dict(j) for j in json_data]
        yield img, bounding_boxes


def play_logged_data(directory: Path, wait_ms: int = 0, loop_forever: bool = False) -> None:
    """
    Utility function used to playback logged data.

    Args:
        directory: Path to the directory where the data are stored.
        wait_ms: How many milliseconds to wait between each consecutive frames?
        loop_forever: If set to `True` will restart the playback of data.
    """
    for img, bbs in logged_data_gen(directory, loop_forever=loop_forever):
        img = plot_bounding_boxes(img, bbs)
        try:
            cv2.imshow(str(directory), img)
            if cv2.waitKey(wait_ms) != -1:
                print("Detected a keypress, exiting...")
                raise KeyboardInterrupt
        except KeyboardInterrupt:
            cv2.destroyAllWindows()
            sys.exit(0)
