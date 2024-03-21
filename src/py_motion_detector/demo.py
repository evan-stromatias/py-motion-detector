import uuid
from pathlib import Path

from src.py_motion_detector.callbacks.directory_frame_dumper import DirectoryFrameDumperCallback
from src.py_motion_detector.callbacks.frame_renderer import FrameRendererCallback
from src.py_motion_detector.input_sources.image_files import ImageFilesFrameProvider
from src.py_motion_detector.models.motion_detection.weighted_average_past_frames import MotionDetectionWeightedAverage
from src.py_motion_detector.motion_detection_app import MotionDetectionApplication

if __name__ == '__main__':
    p_id = str(uuid.uuid4())
    path_to_dir = Path().home() / "Downloads" / "demo"
    input_img_dir = Path().home() / "Downloads" / "video"
    callbacks = [
        FrameRendererCallback(),
        DirectoryFrameDumperCallback(
            path_to_dir / p_id,
            draw_bounding_boxes=True,
        ),
    ]

    input_source = ImageFilesFrameProvider(
        path_to_dir=input_img_dir,
        files_ending_with="png",
    )

    print(f"Starting the motion detection app: {p_id}.")
    motion_app = MotionDetectionApplication(
        frame_provider=input_source,
        motion_detection_model=MotionDetectionWeightedAverage(min_area=500, delta_threshold=10),
        callbacks=callbacks,
    )

    motion_app.run()
