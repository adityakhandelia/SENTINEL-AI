'''Download a sample public-domain video with people for pipeline testing.'''

import argparse
import urllib.request
from pathlib import Path


URLS = {
    'people_walking': 'https://raw.githubusercontent.com/intel-iot-devkit/sample-videos/master/face-demographics-walking-and-pause.mp4',
    'person_bicycle_car': 'https://raw.githubusercontent.com/intel-iot-devkit/sample-videos/master/person-bicycle-car-detection.mp4',
}


def download(name: str, output_dir: Path):
    url = URLS.get(name)
    if not url:
        raise ValueError('Unknown sample: {}'.format(name))
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / '{}.mp4'.format(name)
    if output_path.exists():
        print('Already exists: {}'.format(output_path))
        return output_path
    print('Downloading {}...'.format(url))
    urllib.request.urlretrieve(url, str(output_path))
    print('Saved {}'.format(output_path))
    return output_path


def main():
    parser = argparse.ArgumentParser(description='Download sample video')
    parser.add_argument('--name', default='people_walking', choices=list(URLS.keys()))
    parser.add_argument('--output-dir', default='data/raw')
    args = parser.parse_args()
    download(args.name, Path(args.output_dir))


if __name__ == '__main__':
    main()
