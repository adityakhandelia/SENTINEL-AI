'''Test-data download helper.

For Viva 1 you need at least:
  - 2-3 normal clips (walking, talking, standing)
  - 2-3 fight/aggression clips

Recommended sources:
  - Hockey Fights dataset (academic torrents / Kaggle)
  - RWF-2000 dataset (large, use for final benchmarking in Viva 4)
  - UCF-Crime dataset (literature reference)

Place all clips under data/raw/ and run:
    python backend/cli_demo.py --source data/raw/<clip>.mp4 --output data/processed/<clip>_annotated.mp4
'''

from pathlib import Path


RAW_DIR = Path(__file__).parent.parent / 'data' / 'raw'


def list_missing_clips():
    clips = list(RAW_DIR.glob('*.mp4')) + list(RAW_DIR.glob('*.avi'))
    print('Found {} test clip(s) in {}'.format(len(clips), RAW_DIR))
    for c in clips:
        print('  - {}'.format(c.name))
    if not clips:
        print('Please add normal and fight clips to data/raw/')


if __name__ == '__main__':
    list_missing_clips()
