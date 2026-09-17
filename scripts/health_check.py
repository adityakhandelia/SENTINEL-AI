'''Health check script to verify SENTINEL-AI installation and basic functionality.'''

import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / 'backend'))

import numpy as np


def check_python():
    version = sys.version_info
    ok = version >= (3, 10)
    return ok, 'Python {}.{}.{}'.format(version.major, version.minor, version.micro)


def check_packages():
    required = ['ultralytics', 'cv2', 'numpy', 'scipy', 'pytest', 'pptx']
    missing = []
    for pkg in required:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)
    return len(missing) == 0, 'missing: {}'.format(missing) if missing else 'all present'


def check_model():
    model_path = ROOT / 'yolov8n-pose.pt'
    return model_path.exists(), str(model_path) if model_path.exists() else 'yolov8n-pose.pt not found (will auto-download on first run)'


def check_test_videos():
    raw = ROOT / 'data' / 'raw'
    videos = list(raw.glob('*.mp4'))
    return len(videos) > 0, '{} video(s) found'.format(len(videos))


def run_pytest():
    result = subprocess.run([sys.executable, '-m', 'pytest', '-q'], cwd=str(ROOT), capture_output=True, text=True)
    ok = result.returncode == 0
    return ok, result.stdout[-500:] if not ok else 'all tests passed'


def check_inference():
    try:
        from app.vision.pose_estimator import PoseEstimator
        estimator = PoseEstimator()
        blank = np.zeros((480, 640, 3), dtype=np.uint8)
        result = estimator.predict(blank, conf=0.3)
        return True, 'inference ok, persons={}'.format(len(result['persons']))
    except Exception as e:
        return False, str(e)


def main():
    checks = [
        ('Python >= 3.10', check_python),
        ('Required packages', check_packages),
        ('YOLOv8n-pose model', check_model),
        ('Test videos in data/raw', check_test_videos),
        ('Unit tests (pytest)', run_pytest),
        ('YOLO inference smoke test', check_inference),
    ]

    print('=' * 60)
    print('SENTINEL-AI Health Check')
    print('=' * 60)

    passed = 0
    for name, fn in checks:
        ok, msg = fn()
        status = 'PASS' if ok else 'FAIL'
        print('[{}] {} - {}'.format(status, name, msg))
        if ok:
            passed += 1

    print('=' * 60)
    print('Result: {}/{} checks passed'.format(passed, len(checks)))
    if passed == len(checks):
        print('System is ready for Viva 1 demo.')
    else:
        print('Please fix the failed checks before proceeding.')


if __name__ == '__main__':
    main()
