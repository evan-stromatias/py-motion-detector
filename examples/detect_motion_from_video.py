"""Example using a video file as an input source and rendering images to a window callback in real-time."""

from pathlib import Path

from src.py_motion_detector.callbacks.frame_renderer import FrameRendererCallback
from src.py_motion_detector.input_sources.video_file import VideoFileFrameProvider
from src.py_motion_detector.models.motion_detection.weighted_average_past_frames import MotionDetectionWeightedAverage
from src.py_motion_detector.motion_detection_app import MotionDetectionApplication


def main():
    input_video_path = Path().cwd() / "videos" / "garden.mp4"
    callbacks = [
        FrameRendererCallback(),
    ]

    input_source = VideoFileFrameProvider(path_to_video_file=input_video_path)

    motion_app = MotionDetectionApplication(
        frame_provider=input_source,
        motion_detection_model=MotionDetectionWeightedAverage(min_area=500, delta_threshold=10),
        callbacks=callbacks,
    )

    motion_app.run()


if __name__ == '__main__':
    main()
