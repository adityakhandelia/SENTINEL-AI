'''Motion analysis: joint velocity and acceleration heuristics.'''

from typing import Dict, Any, List, Optional
import numpy as np


class MotionAnalyzer:
    '''Computes frame-to-frame joint velocities and flags suspicious motion.'''

    def __init__(self, velocity_threshold: float = 40.0,
                 joints_of_interest: Optional[List[int]] = None):
        self.velocity_threshold = velocity_threshold
        self.joints_of_interest = joints_of_interest or [9, 10]
        self.prev_keypoints: List[np.ndarray] = []

    def reset(self) -> None:
        self.prev_keypoints = []

    def update(self, pose_result: Dict[str, Any]) -> Dict[str, Any]:
        persons = pose_result.get('persons', [])
        velocities: List[Optional[float]] = []
        flags: List[bool] = []
        max_velocity = 0.0

        if len(persons) != len(self.prev_keypoints):
            self.prev_keypoints = [np.array(p.get('keypoints', [])) for p in persons]
            return {
                'max_velocity': 0.0,
                'per_person_velocity': [0.0] * len(persons),
                'suspicious_flags': [False] * len(persons),
                'any_suspicious': False
            }

        for i, person in enumerate(persons):
            kpts = np.array(person.get('keypoints', []))
            if kpts.shape[0] == 0:
                velocities.append(None)
                flags.append(False)
                continue

            velocity = 0.0
            flag = False
            prev = self.prev_keypoints[i]
            if prev.shape[0] == kpts.shape[0]:
                dx = kpts[:, 0] - prev[:, 0]
                dy = kpts[:, 1] - prev[:, 1]
                dist = np.sqrt(dx * dx + dy * dy)
                velocity = float(np.max(dist))
                selected = dist[self.joints_of_interest]
                flag = bool(np.max(selected) > self.velocity_threshold)

            velocities.append(velocity)
            flags.append(flag)
            max_velocity = max(max_velocity, velocity)

        self.prev_keypoints = [np.array(p.get('keypoints', [])) for p in persons]
        return {
            'max_velocity': max_velocity,
            'per_person_velocity': velocities,
            'suspicious_flags': flags,
            'any_suspicious': any(flags)
        }
