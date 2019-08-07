# https://www.pyimagesearch.com/2015/06/01/home-surveillance-and-motion-detection-with-the-raspberry-pi-python-and-opencv/
from typing import List, Optional
import datetime
import time
import cv2
import logging
import sys

from py_motion_detector.callbacks.callback_abc import MotionDetectionCallbackABC
from py_motion_detector.callbacks.directory_frame_dumper import DirectoryFrameDumperCallbackABC
from py_motion_detector.callbacks.object_plotter import ObjectPlotterCallback
from py_motion_detector.models.motion_detection.motion_detection_model_abc import MotionDetectionModelABC
from py_motion_detector.models.motion_detection.weighted_average_past_frames import MotionDetectionWeightedAverage

logger = logging.getLogger(__name__)


class MotionDetectionApplication:
    def __init__(self, from_time: Optional[datetime.time] = None, duration: Optional[datetime.time] = None, motion_detection_model: Optional[MotionDetectionModelABC] = None, callbacks: Optional[List[MotionDetectionCallbackABC]] = None, resize_frame_to=None, video_capture_index=0):
        self.from_time = from_time
        self.duration = duration
        self.video_capture = cv2.VideoCapture(video_capture_index)
        self.resize_frame_to = resize_frame_to
        self.motion_detection_model = motion_detection_model if motion_detection_model is not None else MotionDetectionWeightedAverage()
        self.callbacks = callbacks if callbacks is not None else []
        self.sleep_sec = 10

    def run(self):
        logger.info("Starting Motion Detection App")
        _ = [callback.on_start() for callback in self.callbacks]
        try:
            while True:

                if self.should_process_based_on_time() is not True:
                    logger.info("Skipping processing frames because current time not between {} and duration {}. Sleeping for {} seconds".format(
                        self.from_time, self.duration, self.sleep_sec))
                    time.sleep(self.sleep_sec)
                    continue

                frame = self.video_capture.read()
                frame = frame[1]

                if frame is None:
                    continue

                frame = cv2.resize(frame, (self.resize_frame_to, self.resize_frame_to)) \
                    if self.resize_frame_to is not None \
                    else frame

                motion_detected_bounding_boxes = self.motion_detection_model.next_frame(frame)

                timestamp = datetime.datetime.now()
                for callback in self.callbacks:
                    callback.execute(frame=frame, timestamp=timestamp, bounding_boxes=motion_detected_bounding_boxes)

        except KeyboardInterrupt:
            logger.info("Exiting Motion Detection App")
        except Exception as e:
            logger.exception("Uncaught exception: {}".format(e))
            logger.exception("Exiting with error code 1")
            sys.exit(1)
        finally:
            logger.info("Executing the on_exit method of the callback classes")
            _ = [callback.on_exit() for callback in self.callbacks]

    def should_process_based_on_time(self):
        if self.from_time is None or self.duration is None:
            return True
        current_time = datetime.datetime.now()
        from_datetime = datetime.datetime.combine(current_time.date(), self.from_time)
        until = from_datetime + datetime.timedelta(hours=self.duration.hour, minutes=self.duration.minute, seconds=self.duration.second)
        if from_datetime <= current_time < until:
            return True
        else:
            return False


if __name__ == '__main__':
    motion_app = MotionDetectionApplication(
        # from_time=datetime.datetime.strptime("19:50:00", '%H:%M:%S').time(),
        # duration=datetime.datetime.strptime("5", '%M').time(),
        callbacks=[
        # DirectoryFrameDumperCallbackABC("/tmp/evan/")
    # ],
        ObjectPlotterCallback()],
        resize_frame_to=500)
    motion_app.run()
