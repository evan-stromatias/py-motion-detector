import datetime
import sys
import time
from typing import List

import structlog

from py_motion_detector.callbacks.base import MotionDetectionCallbackABC
from py_motion_detector.input_sources.base import FrameProviderABC
from py_motion_detector.models.motion_detection.base import MotionDetectionModelABC
from py_motion_detector.models.motion_detection.weighted_average_past_frames import MotionDetectionWeightedAverage

logger = structlog.get_logger()


class MotionDetectionApplication:
    """
    Entry point of the Motion Detection App.
    Users can define callback classes to respond to motion detected events. The default callback used here is to store
    the frames where motion has been detected in a user-defined directory along with the bounding boxes stored as JSON.

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

    def __init__(
        self,
        frame_provider: FrameProviderABC,
        from_time: datetime.time | None = None,
        duration: datetime.time | None = None,
        motion_detection_model: MotionDetectionModelABC | None = None,
        callbacks: List[MotionDetectionCallbackABC] | None = None,
        sleep_sec: int = 10,
    ):
        """

        Args:
            frame_provider: An object that can be used to provide input frames.
            from_time: From what time to start detecting motion.
            duration: Until what time to run the motion detection app.
            motion_detection_model: An object that implements a motion detection algorithm.
            callbacks: List of callbacks that are called at the beginning, and when an object is detected by the
                motion detection algorithm
            sleep_sec: How many seconds to sleep if outside of the `from_time` and `duration`. TODO
        """
        self.from_time = from_time
        self.duration = duration
        self.frame_provider = frame_provider
        self.motion_detection_model = (
            motion_detection_model if motion_detection_model is not None else MotionDetectionWeightedAverage()
        )
        self.callbacks = callbacks if callbacks is not None else []
        self.sleep_sec = sleep_sec

    def run(self):
        """The main entry point of the app."""
        self._setup_callbacks()
        try:
            self._run()
        except KeyboardInterrupt:
            logger.info("Exiting Motion Detection App")
            sys.exit(0)
        except Exception as e:
            logger.exception(f"Uncaught exception: {e}")
            logger.exception("Exiting with error code 1")
            sys.exit(1)
        finally:
            self._shutdown_callbacks()

    def _setup_callbacks(self):
        """This method is called before the main application runs to set up all callback classes"""
        logger.info("Setting up the Callback Classes.")
        _ = [callback.on_start() for callback in self.callbacks]

    def _shutdown_callbacks(self):
        """This method is called when the main application closes to shut down all callback classes"""
        logger.info("Shutting down the Callback Classes.")
        _ = [callback.on_exit() for callback in self.callbacks]

    def _run(self):
        logger.info("Starting Motion Detection App")

        with self.frame_provider as frame_prv:
            for frame in frame_prv.frames():

                if self._should_process_based_on_time() is not True:
                    logger.info(
                        f"Skipping processing frames because current time not between {self.from_time} "
                        f"and duration {self.duration}. Sleeping for {self.sleep_sec} seconds"
                    )
                    time.sleep(self.sleep_sec)
                    continue

                motion_detected_bounding_boxes = self.motion_detection_model.next_frame(frame)

                timestamp = datetime.datetime.now()
                for callback in self.callbacks:
                    callback.execute(frame=frame, timestamp=timestamp, bounding_boxes=motion_detected_bounding_boxes)

    def _should_process_based_on_time(self) -> bool:
        if self.from_time is None or self.duration is None:
            return True

        current_time = datetime.datetime.now()
        from_datetime = datetime.datetime.combine(current_time.date(), self.from_time)
        until = from_datetime + datetime.timedelta(
            hours=self.duration.hour, minutes=self.duration.minute, seconds=self.duration.second
        )
        return True if from_datetime <= current_time < until else False
