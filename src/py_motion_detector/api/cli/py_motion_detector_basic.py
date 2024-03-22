"""Main entry point of the `py_motion_detector` CLI."""

import argparse
import logging
import uuid
from pathlib import Path

import structlog

from py_motion_detector.callbacks.frame_file_dumper import FrameFileDumperCallback
from py_motion_detector.common.parsers import str2time_duration, str2time_start_processing_time
from py_motion_detector.input_sources.camera import CameraFrameProvider
from py_motion_detector.models.motion_detection.weighted_average_past_frames import MotionDetectionWeightedAverage
from py_motion_detector.motion_detection_app import MotionDetectionApplication


def parse_args() -> argparse.Namespace:
    """Parsing the command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        "--path-to-dir",
        type=Path,
        help="Path to directory to store frames [default=/tmp/motion_detector/]",
        required=True,
    )
    parser.add_argument(
        "-r", "--resize-camera-frames", type=int, help="Resize camera captured frames [default=500]", default=500
    )
    parser.add_argument(
        "-m",
        "--min-area",
        type=int,
        help="Motion detection with weighted average past frames, minimum area to be detected [default=5000]",
        default=5000,
    )
    parser.add_argument(
        "-t",
        "--delta-threshold",
        type=int,
        help="Motion detection with weighted average past frames, threshold value for the difference between current "
        "frame and weighted average [default=5]",
        default=5,
    )
    parser.add_argument(
        "-c", "--opencv-video-capture-index", type=int, help="Index of the camera for OpenCV [default=0]", default=0
    )
    parser.add_argument(
        "-i",
        "--log-info",
        type=str,
        help="Log level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
    )
    parser.add_argument(
        "-s",
        "--start_processing_time",
        type=str2time_start_processing_time,
        help="Enable motion tracking from a specific time, using the following format: "
        "hh:mm:ss [default=None means always on]",
        default=None,
    )
    parser.add_argument(
        "-d",
        "--processing_duration",
        type=str2time_duration,
        help="Duration that the motion detector is going to be active. "
        "Format #h/m/s where # is a number and h=hours, m=minutes, s=seconds [default=24h]",
        default=None,
    )
    return parser.parse_args()


def main() -> None:
    p_id = str(uuid.uuid4())
    args = parse_args()

    args.path_to_dir.mkdir(parents=True, exist_ok=True)
    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(logging.getLevelName(args.log_info)),
        logger_factory=structlog.WriteLoggerFactory(file=(args.path_to_dir / p_id).with_suffix(".log").open("wt")),
    )

    callbacks = [FrameFileDumperCallback(args.path_to_dir / p_id)]

    input_source = CameraFrameProvider(
        resize_frame=args.resize_camera_frames, video_capture_index=args.opencv_video_capture_index
    )

    print(f"Starting the motion detection app: {p_id}.")
    motion_app = MotionDetectionApplication(
        frame_provider=input_source,
        from_time=args.start_processing_time,
        duration=args.processing_duration,
        motion_detection_model=MotionDetectionWeightedAverage(
            min_area=args.min_area, delta_threshold=args.delta_threshold
        ),
        callbacks=callbacks,
    )

    motion_app.run()


if __name__ == '__main__':
    main()
