from pathlib import Path
from typing import Dict, List

from pandas import DataFrame


def parse_coord(coord: str) -> List[float]:
    coords = coord.split(' ', 3)
    return list(float(coord.strip('XYZ=')) for coord in coords)


def parse_line(line: str):
    event, actor_id, timestamp, coordinates = line.split(',', 4)
    return tuple([event, actor_id, timestamp] + parse_coord(coordinates))


def parse(file_path: str) -> DataFrame:
    with open(file_path, 'r') as f:
        return DataFrame.from_records(
            [parse_line(line) for line in f.readlines()],
            columns=['event', 'id', 'timestamp', 'x', 'y', 'z'])


def parse_name(filename) -> Dict:
    stem: str = Path(filename).stem
    splits = stem.split(sep='-', maxsplit=5)
    return {'map': str(splits[0]), 'algorithm': str(splits[1]),
            'robots': int(splits[2]), 'resources': int(splits[3]),
            'simulation': int(splits[4])}
