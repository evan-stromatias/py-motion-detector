import sys
import os
import glob
import json
from itertools import cycle

import cv2

from py_motion_detector.models.bounding_box import BoundingBox
from py_motion_detector.common.plotting import plot_bounding_boxes


def logged_data_gen(directory: str, img_ending="*.jpg", loop_forever: bool = False):
    images = glob.glob(os.path.join(directory, img_ending))
    images = sorted(images)
    if loop_forever is True:
        images = cycle(images)
    for img_p in images:
        img = cv2.imread(img_p)
        json_data = []
        json_p = os.path.join(directory, os.path.basename(img_p).split(".")[0]+".json")
        try:
            with open(json_p) as f:
                json_data = json.load(f)
        except FileNotFoundError:
            pass
        bounding_boxes = [BoundingBox.from_dict(j) for j in json_data]
        yield img, bounding_boxes


def play_logged_data(directory: str, wait_key=0, loop_forever=False):
    for img, bbs in logged_data_gen(directory, loop_forever=loop_forever):
        img = plot_bounding_boxes(img, bbs)
        try:
            cv2.imshow(directory, img)
            cv2.waitKey(wait_key)
        except KeyboardInterrupt:
            cv2.destroyAllWindows()
            sys.exit(0)


if __name__ == '__main__':
    play_logged_data("/tmp/bgf/")
