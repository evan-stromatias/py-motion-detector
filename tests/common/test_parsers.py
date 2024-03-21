import datetime
import unittest

from py_motion_detector.common.parsers import str2time_duration


class TestParsers(unittest.TestCase):
    def setUp(self):
        self.duration_str10h = "10h"
        self.duration_str10m = "10m"
        self.duration_str10s = "10s"
        self.duration_str1incorrect = "1q"
        self.duration_str = "lala"

        self.duration_time10h = datetime.datetime.strptime("10", "%H").time()
        self.duration_time10m = datetime.datetime.strptime("10", "%M").time()
        self.duration_time10s = datetime.datetime.strptime("10", "%S").time()

    def tearDown(self):
        pass

    def test_str2time_duration(self):
        duration_time = str2time_duration(self.duration_str10h)
        self.assertEqual(self.duration_time10h, duration_time)

        duration_time = str2time_duration(self.duration_str10m)
        self.assertEqual(self.duration_time10m, duration_time)

        duration_time = str2time_duration(self.duration_str10s)
        self.assertEqual(self.duration_time10s, duration_time)

    def test_str2time_duration_none(self):
        duration_time = str2time_duration(None)
        self.assertEqual(None, duration_time)

    def test_str2time_duration_incorrect_unit(self):
        self.assertRaises(ValueError, str2time_duration, self.duration_str1incorrect)

    def test_str2time_duration_incorrect(self):
        self.assertRaises(ValueError, str2time_duration, self.duration_str)
