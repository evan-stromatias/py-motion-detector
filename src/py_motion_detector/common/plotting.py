import datetime
from typing import List

import cv2
import numpy as np

from py_motion_detector.models.bounding_box import BoundingBox


def plot_bounding_boxes(image: np.array, bounding_boxes: List[BoundingBox], color=(0, 255, 0)) -> np.array:
    """
    Plots bounded boxes on an image using a user-specified color.

    Args:
        image: An input image.
        bounding_boxes: A list of bounding boxes that will be plotted on the image.
        color: The color that will be used to draw the bounding boxes on the image

    Returns:
        Returns a new image with bounding boxes. The original `image` is not modified.
    """
    frame = image.copy()
    for bb in bounding_boxes:
        cv2.rectangle(frame, (bb.left, bb.top), (bb.right, bb.bottom), color, 2)
    return frame


def plot_timestamp_to_frame(image: np.array, timestamp: datetime.datetime, color=(0, 0, 255)):
    """
    Plots a timestamp to an input image using a user-specified color.

    Args:
        image: An input image.
        timestamp: A timestamp that will be plotted on the image.
        color: The color that will be used to draw the timestamp on the image

    Returns:
        Returns a new image with a timestamp. The original `image` is not modified.
    """
    frame = image.copy()
    ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
    cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)
    return frame
