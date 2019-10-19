import abc

import cv2
import numpy as np


class FrameProviderABC(abc.ABC):
    @abc.abstractmethod
    def next_frame(self) -> np.array:
        """

        :return: Next frame from the input source
        """
        pass

    @abc.abstractmethod
    def on_exit(self):
        pass

    @property
    @abc.abstractmethod
    def has_finished(self) -> bool:
        """
        If the source has stopped producing frames should return false
        :return:
        """
        pass

    @property
    @abc.abstractmethod
    def resize_to(self) -> int:
        """

        :return: Integer value to resize the frame
        """

    def resize_frame(self, frame: np.array) -> np.array:
        frame = cv2.resize(frame, (self.resize_to, self.resize_to)) \
            if self.resize_to and frame is not None \
            else frame
        return frame
