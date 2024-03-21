import unittest

import numpy as np
from py_motion_detector.models.motion_detection.weighted_average_past_frames import MotionDetectionWeightedAverage


class TestMotionDetectionWeightedAverage(unittest.TestCase):
    def setUp(self):
        frame_shape = (800, 800, 3)
        self.frame_zeros = np.zeros(frame_shape).astype("uint8")
        self.frame_ones = (np.ones(frame_shape) * 255).astype("uint8")

        self.motion_detection_model = MotionDetectionWeightedAverage()

    def tearDown(self):
        self.motion_detection_model = MotionDetectionWeightedAverage()

    def test_next_frame_no_change_zeros(self):
        frames = [self.frame_zeros, self.frame_zeros, self.frame_zeros]
        for frame in frames:
            bbs = self.motion_detection_model.next_frame(frame)
            self.assertEqual(bbs, [])

    def test_next_frame_no_change_ones(self):
        frames = [self.frame_ones, self.frame_ones, self.frame_ones]
        for frame in frames:
            bbs = self.motion_detection_model.next_frame(frame)
            self.assertEqual(bbs, [])

    def test_next_frame(self):
        frames = [self.frame_zeros, self.frame_zeros, self.frame_ones]
        bounding_boxes = []
        for frame in frames:
            bbs = self.motion_detection_model.next_frame(frame)
            bounding_boxes.append(bbs)

        self.assertEqual(len(bounding_boxes[0]), 0)
        self.assertEqual(len(bounding_boxes[1]), 0)
        self.assertEqual(len(bounding_boxes[2]), 1)

    def test_next_frame_less_than_min_area(self):
        frame_shape = (32, 32, 3)
        frame_zeros = np.zeros(frame_shape).astype("uint8")
        frame_ones = (np.ones(frame_shape) * 255).astype("uint8")
        motion_detection_model = MotionDetectionWeightedAverage(min_area=32 * 32 + 1)
        frames = [frame_zeros, frame_zeros, frame_ones]
        for frame in frames:
            bbs = motion_detection_model.next_frame(frame)
            self.assertEqual(bbs, [])
