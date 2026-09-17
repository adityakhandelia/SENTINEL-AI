'''One-command demo runner for Viva 1.'''

import subprocess
from pathlib import Path

ROOT = Path(__file__).parent.parent
PYTHON = str(ROOT / '.venv' / 'Scripts' / 'python.exe')


def run(cmd):
    print('>> {}'.format(' '.join(str(c) for c in cmd)))
    result = subprocess.run(cmd, cwd=str(ROOT))
    return result.returncode == 0


def ensure_normal_clip():
    clip = ROOT / 'data' / 'raw' / 'people_walking_demo.mp4'
    if clip.exists():
        return clip
    full = ROOT / 'data' / 'raw' / 'people_walking.mp4'
    if not full.exists():
        if not run([PYTHON, 'scripts/download_sample_video.py']):
            return None
    if not run([PYTHON, 'scripts/clip_video.py', '--source', 'data/raw/people_walking.mp4',
                '--output', 'data/raw/people_walking_demo.mp4', '--duration', '10']):
        return None
    return clip


def main():
    print('=' * 60)
    print('SENTINEL-AI Viva 1 Demo Runner')
    print('=' * 60)

    print('\n--- 1. Health check ---')
    if not run([PYTHON, 'scripts/health_check.py']):
        print('Health check failed. Aborting.')
        return

    print('\n--- 2. Ensure demo clip ---')
    clip = ensure_normal_clip()
    if clip is None:
        print('Could not prepare demo clip. Aborting.')
        return

    print('\n--- 3. Run CLI demo on normal clip ---')
    output = ROOT / 'data' / 'processed' / 'demo_output.mp4'
    if not run([PYTHON, 'backend/cli_demo.py', '--source', str(clip), '--output', str(output)]):
        print('CLI demo failed.')
        return

    print('\n--- 4. Demo complete ---')
    print('Output video: {}'.format(output))
    print('Open it with any video player to see skeletal overlays.')
    print('\nTo run on a fight clip:')
    print('  {} backend/cli_demo.py --source data/raw/fight.mp4 --output data/processed/fight_annotated.mp4'.format(PYTHON))


if __name__ == '__main__':
    main()
