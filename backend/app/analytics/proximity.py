'''Proximity analysis: inter-person distance and close-pair detection.'''

from typing import Dict, Any, List, Optional, Tuple
import numpy as np


def _centroid(keypoints: List[List[float]]) -> Optional[np.ndarray]:
    arr = np.array(keypoints)
    visible = arr[arr[:, 2] > 0.3]
    if len(visible) == 0:
        return None
    return visible[:, :2].mean(axis=0)


class ProximityAnalyzer:
    '''Detects when two or more people are close to each other.'''

    def __init__(self, distance_threshold: float = 150.0):
        self.distance_threshold = distance_threshold

    def analyze(self, pose_result: Dict[str, Any]) -> Dict[str, Any]:
        persons = pose_result.get('persons', [])
        centroids = []
        for p in persons:
            c = _centroid(p.get('keypoints', []))
            centroids.append(c)

        pairs: List[Tuple[int, int]] = []
        distances: List[Dict[str, Any]] = []
        for i in range(len(centroids)):
            for j in range(i + 1, len(centroids)):
                if centroids[i] is None or centroids[j] is None:
                    continue
                d = float(np.linalg.norm(centroids[i] - centroids[j]))
                distances.append({'pair': (i, j), 'distance': d})
                if d < self.distance_threshold:
                    pairs.append((i, j))

        return {
            'centroids': centroids,
            'pairs': pairs,
            'distances': distances,
            'any_close': len(pairs) > 0
        }
