'''Unit tests for proximity analytics.'''

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.analytics.proximity import ProximityAnalyzer


def make_person_at(x: float, y: float) -> dict:
    keypoints = [[x, y, 1.0] for _ in range(17)]
    return {'keypoints': keypoints, 'bbox': [x, y, x + 100, y + 200], 'confidence': 0.9}


def test_close_pair_detected():
    a = ProximityAnalyzer(distance_threshold=150.0)
    p1 = make_person_at(100.0, 100.0)
    p2 = make_person_at(120.0, 120.0)
    r = a.analyze({'persons': [p1, p2]})
    assert r['any_close'] is True
    assert (0, 1) in r['pairs']


def test_far_pair_not_detected():
    a = ProximityAnalyzer(distance_threshold=150.0)
    p1 = make_person_at(100.0, 100.0)
    p2 = make_person_at(500.0, 500.0)
    r = a.analyze({'persons': [p1, p2]})
    assert r['any_close'] is False
    assert len(r['pairs']) == 0
