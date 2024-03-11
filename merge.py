import sys
import json

def merge(title: str) -> None:
    from utils import load_profiler

    local_file = f'{title}_edge.json'
    cloud_file = f'{title}_size.json'
    with open(local_file, 'r') as file:
        ldict = json.load(file)
    with open(cloud_file, 'r') as file:
        rdict = json.load(file)
    lrdict = load_profiler.merge_profile(ldict, rdict)
    with open(local_file, 'w') as file:
        json.dump(lrdict, file, indent=4)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: merge.py <title>', file=sys.stderr)
    merge(sys.argv[1])