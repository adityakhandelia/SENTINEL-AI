'''SENTINEL-AI Viva 1 CLI demo.'''

import argparse
import sys
import time
from pathlib import Path

import cv2

sys.path.insert(0, str(Path(__file__).parent))

from app.ingest.video_reader import VideoReader
from app.vision.pose_estimator import PoseEstimator
from app.vision.renderer import Renderer
from app.analytics.motion import MotionAnalyzer
from app.analytics.proximity import ProximityAnalyzer


def main() -> None:
    parser = argparse.ArgumentParser(description='SENTINEL-AI Viva 1 CLI Demo')
    parser.add_argument('--source', required=True, help='video file path or 0 for webcam')
    parser.add_argument('--output', default='data/processed/output_annotated.mp4', help='output annotated video path')
    parser.add_argument('--device', default='cpu', help='cpu or cuda')
    parser.add_argument('--conf', type=float, default=0.3, help='pose confidence threshold')
    parser.add_argument('--show', action='store_true', help='show live preview')
    args = parser.parse_args()

    source = 0 if args.source == '0' else args.source

    reader = VideoReader(source)
    estimator = PoseEstimator(device=args.device)
    renderer = Renderer()
    motion = MotionAnalyzer(velocity_threshold=30.0)
    proximity = ProximityAnalyzer(distance_threshold=150.0)

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(args.output, fourcc, int(reader.fps), (reader.width, reader.height))

    print('Processing {} -> {}'.format(args.source, args.output))
    print('Resolution: {}x{} @ {:.2f} FPS'.format(reader.width, reader.height, reader.fps))

    start = time.time()
    frame_id = 0
    for frame_id, frame, timestamp in reader:
        pose_result = estimator.predict(frame, conf=args.conf)
        motion_result = motion.update(pose_result)
        prox_result = proximity.analyze(pose_result)

        if motion_result['any_suspicious'] and prox_result['any_close']:
            threat = 'FIGHT'
            color = (0, 0, 255)
        elif motion_result['any_suspicious']:
            threat = 'WARNING'
            color = (0, 255, 255)
        else:
            threat = 'NORMAL'
            color = (0, 255, 0)

        annotated = renderer.render(
            frame, pose_result,
            motion_flags=motion_result['suspicious_flags'],
            proximity_pairs=prox_result['pairs']
        )
        cv2.putText(annotated, '{} max_v={:.1f}'.format(threat, motion_result['max_velocity']),
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        writer.write(annotated)
        if args.show:
            cv2.imshow('SENTINEL-AI', annotated)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        if frame_id % 30 == 0:
            print('frame {} | persons={} | {} | max_v={:.1f}'.format(
                frame_id, len(pose_result['persons']), threat, motion_result['max_velocity']))

    reader.release()
    writer.release()
    cv2.destroyAllWindows()
    elapsed = time.time() - start
    fps_processed = frame_id / elapsed if elapsed > 0 else 0
    print('Done in {:.1f}s (~{:.1f} FPS processed)'.format(elapsed, fps_processed))


if __name__ == '__main__':
    main()
