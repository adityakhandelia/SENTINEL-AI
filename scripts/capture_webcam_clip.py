'''Capture a short clip from the default webcam for real demo data.'''

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'backend'))

import cv2
from app.ingest.video_reader import VideoReader


def main():
    parser = argparse.ArgumentParser(description='Capture webcam clip')
    parser.add_argument('--output', default='data/raw/webcam_clip.mp4')
    parser.add_argument('--duration', type=float, default=5.0)
    args = parser.parse_args()

    reader = VideoReader(0)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    writer = cv2.VideoWriter(args.output, fourcc, int(reader.fps), (reader.width, reader.height))

    print('Recording {:.1f}s from webcam... Press q to stop early.'.format(args.duration))
    max_frames = int(args.duration * reader.fps)
    for frame_id, frame, _ in reader:
        writer.write(frame)
        cv2.imshow('Recording - press q to stop', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if frame_id >= max_frames:
            break

    reader.release()
    writer.release()
    cv2.destroyAllWindows()
    print('Saved {}'.format(args.output))


if __name__ == '__main__':
    main()
