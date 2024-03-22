"""Main entry point of the `py_motion_detector_data_player` CLI used for playing logged data."""

import argparse
from pathlib import Path

from py_motion_detector.utils.logged_data_player import play_logged_data


def parse_args() -> argparse.Namespace:
    """Parsing the command line arguments"""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        "--path-to-logged-data",
        type=Path,
        help="Path to directory where frames (and bounding boxes) are stored.",
        required=True,
    )
    parser.add_argument(
        "-w",
        "--wait-ms",
        type=int,
        help="How many milliseconds to wait before changing a frame in the player [default=1]",
        default=1,
    )
    parser.add_argument(
        "-l", "--loop", action='store_true', help="Loop logged frames forever [default=False]", default=False
    )
    return parser.parse_args()


def main():
    args = parse_args()
    play_logged_data(directory=args.path_to_logged_data, wait_ms=args.wait_ms, loop_forever=args.loop)


if __name__ == '__main__':
    main()
