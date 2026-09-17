'''Video capture module for file, webcam, and RTSP sources.'''

from pathlib import Path
from typing import Iterator, Tuple, Optional, Union
import cv2
import numpy as np


class VideoReader:
    '''OpenCV-based video source wrapper.'''

    def __init__(self, source: Union[str, int], target_fps: Optional[int] = None):
        self.source = source
        if isinstance(source, str) and source.isdigit():
            source = int(source)
        self.cap = cv2.VideoCapture(source)
        if not self.cap.isOpened():
            raise RuntimeError('Cannot open video source: {}'.format(source))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 30.0
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if target_fps:
            self.cap.set(cv2.CAP_PROP_FPS, target_fps)

    def __iter__(self) -> Iterator[Tuple[int, np.ndarray, float]]:
        frame_id = 0
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            timestamp = frame_id / self.fps if self.fps else 0.0
            yield frame_id, frame, timestamp
            frame_id += 1

    def release(self) -> None:
        self.cap.release()
