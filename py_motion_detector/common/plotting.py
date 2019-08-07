import datetime
from typing import List

import cv2
import numpy as np

from py_motion_detector.models.bounding_box import BoundingBox


def plot_bounding_boxes(frame: np.array, bounding_boxes: List[BoundingBox]):
    frame = frame.copy()
    for bb in bounding_boxes:
        cv2.rectangle(frame, (bb.left, bb.top),
                      (bb.right, bb.bottom), (0, 255, 0), 2)
    return frame


def plot_timestamp_to_frame(frame: np.array, timestamp: datetime.datetime):
    frame = frame.copy()
    ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
    cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                0.75, (0, 0, 255), 2)
    return frame
