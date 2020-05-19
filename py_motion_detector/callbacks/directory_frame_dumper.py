import datetime
import os
from typing import List
import logging
import json

import cv2
import numpy as np

from py_motion_detector.callbacks.callback_abc import MotionDetectionCallbackABC
from py_motion_detector.common.plotting import plot_timestamp_to_frame, plot_bounding_boxes
from py_motion_detector.models.bounding_box import BoundingBox

logger = logging.getLogger(__name__)


class DirectoryFrameDumperCallback(MotionDetectionCallbackABC):
    """

    """
    def __init__(self, directory_to_store, store_bounding_boxes=True, draw_bounding_boxes=False):
        self.directory_to_store = directory_to_store
        self.draw_bounding_boxes = draw_bounding_boxes
        self.store_bounding_boxes = store_bounding_boxes
        logger.info("Callback class has been initialized")

    def on_start(self):
        if not os.path.exists(self.directory_to_store):
            logger.info("Directory {} does not exist, creating".format(self.directory_to_store))
            os.mkdir(self.directory_to_store)
        logger.info("Storing frames at {}".format(self.directory_to_store))

    def execute(self, frame: np.array, timestamp: datetime.datetime, bounding_boxes: List[BoundingBox]):
        frame = plot_timestamp_to_frame(frame, timestamp)
        if self.draw_bounding_boxes:
            frame = plot_bounding_boxes(frame, bounding_boxes)

        if len(bounding_boxes) > 0:
            logger.info("Number of detected objects {} with object area / frame area = {}".format(
                len(bounding_boxes), [m.area / frame.size for m in bounding_boxes]
            ))

            timestamp = int(datetime.datetime.timestamp(timestamp) * 1000)
            fname = os.path.join(self.directory_to_store, "{}.jpg".format(timestamp))
            cv2.imwrite(fname, frame)

            if self.store_bounding_boxes:
                bboxes = [m.to_dict() for m in bounding_boxes]
                with open(os.path.join(self.directory_to_store, "{}.json".format(timestamp)), 'w') as f:
                    json.dump(bboxes, f, indent=4)

    def on_exit(self):
        logger.info("Exiting callback class")
