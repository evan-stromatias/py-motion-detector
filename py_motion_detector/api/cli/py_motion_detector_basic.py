import argparse
import tempfile
import platform
import logging
import os

from py_motion_detector.common.parsers import str2time_duration, str2time_start_processing_time
from py_motion_detector.motion_detection_app import MotionDetectionApplication
from py_motion_detector.models.motion_detection.weighted_average_past_frames import MotionDetectionWeightedAverage
from py_motion_detector.callbacks.directory_frame_dumper import DirectoryFrameDumperCallbackABC
from py_motion_detector.input_sources.camera import CameraFrameProvider


def parse_args():
    temp_dir = '/tmp' if 'Darwin' in platform.system() else tempfile.gettempdir()

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path-to-dir", type=str, help="Path to directory to store frames [default=/tmp/motion_detector/")
    parser.add_argument("-r", "--resize-camera-frames", type=int, help="Resize camera captured frames [default=500]", default=500)
    parser.add_argument("-m", "--min-area", type=int, help="Motion detection with weighted average past frames, minimum area to be detected [default=5000]", default=5000)
    parser.add_argument("-t", "--delta-threshold", type=int, help="Motion detection with weighted average past frames, threshold value for the difference between current frame and weighted average [default=5]", default=5)
    parser.add_argument("-c", "--opencv-video-capture-index", type=int, help="Index of the camera for OpenCV [default=0]", default=0)
    parser.add_argument("-l", "--log-path", type=str, help="Path to store application logs. [default={}]".format(temp_dir), default=os.path.join(temp_dir, "py_motion_detector.log"))
    parser.add_argument("-i", "--log-info", type=str, help="Log level", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], default="INFO")
    parser.add_argument("-s", "--start_processing_time", type=str, help="Enable motion tracking from a specific time, using the following format: hh:mm:ss [default=None means always on]", default=None)
    parser.add_argument("-d", "--processing_duration", type=str, help="Duration that the motion detector is going to be active. Format #h/m/s where # is a number and h=hours, m=minutes, s=seconds [default=24h]", default=None)
    return parser.parse_args()


def main():
    args = parse_args()

    logging.basicConfig(filename=args.log_path, format="PID:%(process)d Log_Level:%(levelname)s Time:%(asctime)s Module:%(module)s Method:%(funcName)s Message:%(message)s", level=args.log_info)

    callbacks = [
        DirectoryFrameDumperCallbackABC(args.path_to_dir)
    ]

    from_time = str2time_start_processing_time(args.start_processing_time)
    duration = str2time_duration(args.processing_duration)

    input_source = CameraFrameProvider(resize_frame=args.resize_camera_frames,
                                       video_capture_index=args.opencv_video_capture_index)

    motion_app = MotionDetectionApplication(
        input_source=input_source,
        from_time=from_time,
        duration=duration,
        motion_detection_model=MotionDetectionWeightedAverage(min_area=args.min_area, delta_threshold=args.delta_threshold),
        callbacks=callbacks,
    )

    motion_app.run()


if __name__ == '__main__':
    main()
