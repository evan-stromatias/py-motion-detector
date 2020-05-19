# https://www.pyimagesearch.com/2015/06/01/home-surveillance-and-motion-detection-with-the-raspberry-pi-python-and-opencv/
from typing import List, Optional
import datetime
import time
import logging
import sys

from py_motion_detector.input_sources.frame_provider_abc import FrameProviderABC
from py_motion_detector.callbacks.callback_abc import MotionDetectionCallbackABC
from py_motion_detector.models.motion_detection.motion_detection_model_abc import MotionDetectionModelABC
from py_motion_detector.models.motion_detection.weighted_average_past_frames import MotionDetectionWeightedAverage

logger = logging.getLogger(__name__)


class MotionDetectionApplication:
    """
    This is the main Motion Detection App as you probably guessed from the very imaginative name of this class.

    Example usage:

    from py_motion_detector.input_sources.camera import CameraFrameProvider
    from py_motion_detector.models.motion_detection.weighted_average_past_frames import MotionDetectionWeightedAverage

    motion_app = MotionDetectionApplication(
        frame_provider=CameraFrameProvider(resize_frame=500),
        motion_detection_model=MotionDetectionWeightedAverage(min_area=500, delta_threshold=5),
        callbacks=[ObjectPlotterCallback()],
    )
    motion_app.run()
    """
    def __init__(self,
                 frame_provider: FrameProviderABC,
                 from_time: Optional[datetime.time] = None,
                 duration: Optional[datetime.time] = None,
                 motion_detection_model: Optional[MotionDetectionModelABC] = None,
                 callbacks: Optional[List[MotionDetectionCallbackABC]] = None,
                 sleep_sec: int = 10):
        """

        :param frame_provider: An object that can be used to provide input frames (numpy arrays)
        :param from_time: From what time to start recording
        :param duration: For how many hours, minutes, seconds...
        :param motion_detection_model: An object that implements a motion detection algorithm
        :param callbacks: List of callbacks that are called at the beginning, and when an object is detected by the
            motion detection algorithm
        :param sleep_sec: How many seconds to sleep if outside of the `from_time` and `duration`
        """
        self.from_time = from_time
        self.duration = duration
        self.frame_provider = frame_provider
        self.motion_detection_model = motion_detection_model if motion_detection_model is not None else \
            MotionDetectionWeightedAverage()
        self.callbacks = callbacks if callbacks is not None else []
        self.sleep_sec = sleep_sec

    def _run(self):
        logger.info("Starting Motion Detection App")
        _ = [callback.on_start() for callback in self.callbacks]

        with self.frame_provider as frame_prv:
            for frame in frame_prv.frames():

                if self.should_process_based_on_time() is not True:
                    logger.info(
                        "Skipping processing frames because current time not between {} and duration {}. Sleeping for "
                        "{} seconds".format(self.from_time, self.duration, self.sleep_sec))
                    time.sleep(self.sleep_sec)
                    continue

                motion_detected_bounding_boxes = self.motion_detection_model.next_frame(frame)

                timestamp = datetime.datetime.now()
                for callback in self.callbacks:
                    callback.execute(frame=frame, timestamp=timestamp, bounding_boxes=motion_detected_bounding_boxes)

    def run(self):
        try:
            self._run()
        except KeyboardInterrupt:
            logger.info("Exiting Motion Detection App")
        except Exception as e:
            logger.exception("Uncaught exception: {}".format(e))
            logger.exception("Exiting with error code 1")
            sys.exit(1)
        finally:
            logger.info("Executing the on_exit method of the callback classes")
            _ = [callback.on_exit() for callback in self.callbacks]

    def should_process_based_on_time(self) -> bool:
        if self.from_time is None or self.duration is None:
            return True

        current_time = datetime.datetime.now()
        from_datetime = datetime.datetime.combine(current_time.date(), self.from_time)
        until = from_datetime + datetime.timedelta(hours=self.duration.hour, minutes=self.duration.minute,
                                                   seconds=self.duration.second)
        if from_datetime <= current_time < until:
            return True
        else:
            return False
