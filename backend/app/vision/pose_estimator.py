'''YOLOv8-Pose wrapper returning structured keypoint data.'''

from typing import Dict, Any, List
import numpy as np
from ultralytics import YOLO


class PoseEstimator:
    '''Lightweight pose estimator using YOLOv8-Pose.'''

    COCO_KEYPOINTS = [
        'nose', 'left_eye', 'right_eye', 'left_ear', 'right_ear',
        'left_shoulder', 'right_shoulder', 'left_elbow', 'right_elbow',
        'left_wrist', 'right_wrist', 'left_hip', 'right_hip',
        'left_knee', 'right_knee', 'left_ankle', 'right_ankle'
    ]

    def __init__(self, model_name: str = 'yolov8n-pose.pt', device: str = 'cpu'):
        self.model = YOLO(model_name)
        self.device = device

    def predict(self, frame: np.ndarray, conf: float = 0.3) -> Dict[str, Any]:
        results = self.model(frame, device=self.device, conf=conf, verbose=False)
        persons: List[Dict[str, Any]] = []
        if not results:
            return {'persons': persons}
        r = results[0]
        boxes = r.boxes.xyxy.cpu().numpy() if r.boxes is not None else np.empty((0, 4))
        keypoints = r.keypoints
        if keypoints is not None and len(keypoints.data) > 0:
            xy = keypoints.xy.cpu().numpy()
            confs = keypoints.conf.cpu().numpy() if keypoints.conf is not None else np.ones((xy.shape[0], xy.shape[1]))
            for i in range(xy.shape[0]):
                kpts = np.concatenate([xy[i], confs[i][:, None]], axis=1)
                persons.append({
                    'bbox': [float(x) for x in boxes[i]] if i < len(boxes) else None,
                    'keypoints': kpts.tolist(),
                    'confidence': float(np.mean(confs[i]))
                })
        return {'persons': persons}
