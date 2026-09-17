'''Generate a short synthetic test video for pipeline verification.'''

import argparse
import cv2
import numpy as np


def main():
    parser = argparse.ArgumentParser(description='Generate synthetic test video')
    parser.add_argument('--output', default='data/raw/synthetic_test.mp4')
    parser.add_argument('--duration', type=float, default=5.0)
    parser.add_argument('--fps', type=int, default=30)
    parser.add_argument('--width', type=int, default=640)
    parser.add_argument('--height', type=int, default=480)
    args = parser.parse_args()

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(args.output, fourcc, args.fps, (args.width, args.height))
    total_frames = int(args.duration * args.fps)

    for i in range(total_frames):
        frame = np.zeros((args.height, args.width, 3), dtype=np.uint8)
        # color gradient background
        frame[:, :, 0] = int(255 * i / total_frames)
        frame[:, :, 2] = int(255 * (1 - i / total_frames))
        # moving circle
        cx = int(args.width * (0.2 + 0.6 * i / total_frames))
        cy = int(args.height * 0.5)
        cv2.circle(frame, (cx, cy), 30, (0, 255, 0), -1)
        writer.write(frame)

    writer.release()
    print('Wrote {} frames to {}'.format(total_frames, args.output))


if __name__ == '__main__':
    main()
