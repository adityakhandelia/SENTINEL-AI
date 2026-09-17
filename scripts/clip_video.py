'''Extract first N seconds from a video for short demos.'''

import argparse
import pathlib
import cv2


def main():
    parser = argparse.ArgumentParser(description='Clip first N seconds of a video')
    parser.add_argument('--source', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--duration', type=float, default=10.0)
    args = parser.parse_args()

    cap = cv2.VideoCapture(args.source)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    pathlib.Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    writer = cv2.VideoWriter(args.output, fourcc, int(fps), (width, height))

    max_frames = int(args.duration * fps)
    i = 0
    for i in range(max_frames):
        ret, frame = cap.read()
        if not ret:
            break
        writer.write(frame)

    cap.release()
    writer.release()
    print('Clipped {} frames to {}'.format(i, args.output))


if __name__ == '__main__':
    main()
