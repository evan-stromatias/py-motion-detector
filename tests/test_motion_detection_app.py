import datetime
import unittest

import numpy as np
from py_motion_detector.common.parsers import str2time_duration
from py_motion_detector.input_sources.dummy import DummyFrameProvider
from py_motion_detector.motion_detection_app import MotionDetectionApplication


class TestMotionDetectionApplication(unittest.TestCase):
    def setUp(self):
        self.frame = np.random.randint(0, 255, (200, 200), dtype=np.uint8)
        self.dummy_frame_provider = DummyFrameProvider(self.frame, 10)
        self.motion_detection_app = MotionDetectionApplication(frame_provider=self.dummy_frame_provider)

    def test_should_process_based_on_time_5s(self):
        from_time = datetime.datetime.now().time()
        duration = str2time_duration("5s")
        self.motion_detection_app.from_time = from_time
        self.motion_detection_app.duration = duration
        self.assertTrue(self.motion_detection_app.should_process_based_on_time())

    def test_should_process_based_on_time_0s(self):
        from_time = datetime.datetime.now().time()
        duration = str2time_duration("0s")
        self.motion_detection_app.from_time = from_time
        self.motion_detection_app.duration = duration
        self.assertFalse(self.motion_detection_app.should_process_based_on_time())

    def test_should_process_based_on_time_always_process(self):
        self.assertTrue(self.motion_detection_app.should_process_based_on_time())


if __name__ == '__main__':
    unittest.main()
