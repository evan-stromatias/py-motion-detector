import argparse
from py_motion_detector.utils.logged_data_player import play_logged_data


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path-to-logged-data", type=str,
                        help="Path to directory where frames (and bounding boxes) are stored", required=True)
    parser.add_argument("-w", "--wait-for", type=int,
                        help="How many milliseconds to wait before changing a frame in the player [default=1]",
                        default=1)
    parser.add_argument("-l", "--loop", action='store_true', help="Loop logged frames forever [default=False]",
                        default=False)
    return parser.parse_args()


def main():
    args = parse_args()

    play_logged_data(directory=args.path_to_logged_data, wait_key=args.wait_for, loop_forever=args.loop)


if __name__ == '__main__':
    pass
