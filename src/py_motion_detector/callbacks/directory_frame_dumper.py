import datetime
import json
import os
from pathlib import Path
from typing import List

import cv2
import numpy as np
import structlog

from py_motion_detector.callbacks.base import MotionDetectionCallbackABC
from py_motion_detector.common.plotting import plot_bounding_boxes, plot_timestamp_to_frame
from py_motion_detector.models.bounding_box import BoundingBox

logger = structlog.get_logger()


class DirectoryFrameDumperCallback(MotionDetectionCallbackABC):
    def __init__(self, directory_to_store: Path, store_bounding_boxes: bool = True, draw_bounding_boxes: bool = False):
        """
        The default callback used by the command line tool.
        It stores the frames where motion has been detected in a user-defined directory along with their bounding boxes.

        Args:
            directory_to_store: The path of the root directory where images and bounding boxes will be stored.
            store_bounding_boxes: If set to `True` the bounding boxes of the regions where motion was detected will be
                stored to disk.
            draw_bounding_boxes: If set to `True` the bounding boxes of the regions where motion was detected will be
                drawn to the current frame.
        """
        self.directory_to_store = directory_to_store
        self.draw_bounding_boxes = draw_bounding_boxes
        self.store_bounding_boxes = store_bounding_boxes

    def on_start(self):
        """
        Executed when the motion detection application starts and will attempt to create the directory where motion
        data will be stored.
        """
        logger.info(f"Initializing callback class '{self.name()}'.", callback=self.name())
        if not os.path.exists(self.directory_to_store):
            logger.info(
                f"Directory '{self.directory_to_store}' does not exist, attempting to create it...",
                callback=self.name(),
            )
            self.directory_to_store.mkdir(parents=True, exist_ok=True)
            logger.info(f"Directory '{self.directory_to_store}' created.", callback=self.name())
        logger.info(f"Storing frames at '{self.directory_to_store}'.", callback=self.name())
        logger.info(f"Callback class '{self.name()}' has been initialized.", callback=self.name())

    def execute(self, frame: np.array, timestamp: datetime.datetime, bounding_boxes: List[BoundingBox]):
        """
        Executed when a motion has been detected and stores the frames and bounded boxes to disk.

        Args:
            frame: The image for which motion was detected.
            timestamp: The timestamp when a motion was detected.
            bounding_boxes: A list of bounding boxes indicating the regions where motion was detected.
        """
        frame = plot_timestamp_to_frame(frame, timestamp)
        if self.draw_bounding_boxes:
            frame = plot_bounding_boxes(frame, bounding_boxes)

        if len(bounding_boxes):
            object_over_frame_area = [m.area / frame.size for m in bounding_boxes]
            logger.info(
                f"Number of detected objects = {len(bounding_boxes)}. Object area / frame "
                f"area = {object_over_frame_area}",
                callback=self.name(),
            )

            timestamp = int(datetime.datetime.timestamp(timestamp) * 1000)
            file_name = self.directory_to_store / f"{timestamp}.jpg"
            cv2.imwrite(str(file_name), frame)
            logger.debug(f"Image stored at '{file_name}'.", callback=self.name())

            if self.store_bounding_boxes:
                bboxes = [m.to_dict() for m in bounding_boxes]
                json_file_name = self.directory_to_store / f"{timestamp}.json"
                with open(json_file_name, 'w') as f:
                    json.dump(bboxes, f, indent=4)
                    logger.debug(f"Bounding boxes stored at '{json_file_name}'.", callback=self.name())

    def on_exit(self):
        logger.info(f"Shutting down callback class '{self.name()}'.", callback=self.name())
