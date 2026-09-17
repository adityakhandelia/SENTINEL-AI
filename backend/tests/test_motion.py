'''Unit tests for motion analytics.'''

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
from app.analytics.motion import MotionAnalyzer


def make_person(wrist_offset: float = 0.0) -> dict:
    keypoints = [[0.0, 0.0, 1.0] for _ in range(17)]
    keypoints[9] = [50.0 + wrist_offset, 100.0, 1.0]
    keypoints[10] = [150.0 + wrist_offset, 100.0, 1.0]
    return {'keypoints': keypoints, 'bbox': [0, 0, 200, 200], 'confidence': 0.9}


def test_no_motion_is_normal():
    a = MotionAnalyzer(velocity_threshold=30.0)
    p = make_person()
    a.update({'persons': [p]})
    r = a.update({'persons': [p]})
    assert r['max_velocity'] == 0.0
    assert r['any_suspicious'] is False


def test_large_wrist_motion_is_suspicious():
    a = MotionAnalyzer(velocity_threshold=30.0)
    p1 = make_person(0.0)
    p2 = make_person(100.0)
    a.update({'persons': [p1]})
    r = a.update({'persons': [p2]})
    assert r['max_velocity'] > 30.0
    assert r['any_suspicious'] is True


def test_multiple_persons():
    a = MotionAnalyzer(velocity_threshold=30.0)
    p1 = make_person(0.0)
    p2 = make_person(0.0)
    r = a.update({'persons': [p1, p2]})
    assert len(r['per_person_velocity']) == 2
