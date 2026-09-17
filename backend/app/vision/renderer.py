'''Rendering utilities for skeletal overlays and bounding boxes.'''

from typing import Dict, Any, List, Optional, Tuple
import cv2
import numpy as np

COCO_SKELETON = [
    (16, 14), (14, 12), (17, 15), (15, 13), (12, 13),
    (6, 12), (7, 13), (6, 7), (6, 8), (7, 9),
    (8, 10), (9, 11), (2, 3), (1, 2), (1, 3),
    (2, 4), (3, 5), (4, 6), (5, 7)
]

COLOR_NORMAL = (0, 255, 0)
COLOR_WARNING = (0, 255, 255)
COLOR_FIGHT = (0, 0, 255)


def _centroid(keypoints: List[List[float]]) -> Optional[Tuple[int, int]]:
    arr = np.array(keypoints)
    visible = arr[arr[:, 2] > 0.3]
    if len(visible) == 0:
        return None
    c = visible[:, :2].mean(axis=0).astype(int)
    return int(c[0]), int(c[1])


def _draw_skeleton(frame: np.ndarray, keypoints: List[List[float]],
                   color: Tuple[int, int, int], thickness: int = 2) -> None:
    for x, y, conf in keypoints:
        if conf > 0.3:
            cv2.circle(frame, (int(x), int(y)), 3, color, -1)
    for a, b in COCO_SKELETON:
        if a - 1 < len(keypoints) and b - 1 < len(keypoints):
            x1, y1, c1 = keypoints[a - 1]
            x2, y2, c2 = keypoints[b - 1]
            if c1 > 0.3 and c2 > 0.3:
                cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, thickness)


class Renderer:
    '''Draws pose skeletons, bounding boxes, and proximity links.'''

    def __init__(self, keypoint_conf_threshold: float = 0.3):
        self.keypoint_conf_threshold = keypoint_conf_threshold

    def render(self, frame: np.ndarray, pose_result: Dict[str, Any],
               motion_flags: Optional[List[bool]] = None,
               proximity_pairs: Optional[List[Tuple[int, int]]] = None,
               thickness: int = 2) -> np.ndarray:
        output = frame.copy()
        persons = pose_result.get('persons', [])
        motion_flags = motion_flags or [False] * len(persons)

        for i, person in enumerate(persons):
            bbox = person.get('bbox')
            kpts = person.get('keypoints', [])
            color = COLOR_FIGHT if motion_flags[i] else COLOR_NORMAL

            if bbox:
                x1, y1, x2, y2 = map(int, bbox)
                cv2.rectangle(output, (x1, y1), (x2, y2), color, 2)
                label = 'P{} conf={:.2f}'.format(i, person.get('confidence', 0))
                cv2.putText(output, label, (x1, max(y1 - 10, 20)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            _draw_skeleton(output, kpts, color, thickness)

        if proximity_pairs:
            for i, j in proximity_pairs:
                if i < len(persons) and j < len(persons):
                    ci = _centroid(persons[i].get('keypoints', []))
                    cj = _centroid(persons[j].get('keypoints', []))
                    if ci and cj:
                        cv2.line(output, ci, cj, COLOR_WARNING, 2)

        return output
