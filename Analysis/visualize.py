import os
import sys

import matplotlib.pyplot as plt
import seaborn
from joblib import delayed, Memory, Parallel
from pandas import concat

from density import density_over_time
from parse import parse, parse_name
from playback import coordinates_by_timestamp

cache_dir = os.getenv('CACHE_DIR', default='.cache')
memory = Memory(cache_dir)


@memory.cache
def process(log_file, eps=.1, min_samples=2):
    recording = parse(log_file)
    playback = coordinates_by_timestamp(recording)
    raw_densities = density_over_time(playback, eps, min_samples)
    metadata = parse_name(log_file)
    densities = raw_densities.assign(**metadata)
    densities['scaled noise'] = densities['noise'] / densities['resources']
    densities['run'] = densities.apply(
        lambda sample: '{robots} robots, {resources} resources'.format(
            robots=sample['robots'], resources=sample['resources']), axis=1)
    return densities


def main(log_files):
    densities = concat(Parallel(n_jobs=-1, verbose=10)(
        delayed(process)(log_file) for log_file in log_files),
        ignore_index=True)

    plt.figure(figsize=(14, 6), dpi=300)
    seaborn.set_theme()

    seaborn.relplot(data=densities[densities['scaled noise'] <= 1.0],
                    kind='line', x='timestamp',
                    y='scaled noise',
                    hue='algorithm', units='simulation', estimator=None,
                    col='map', style='run').set(
        ylabel='Proportion of Non-Clustered Points', xlabel='Time (s)')

    plt.show()


if __name__ == '__main__':
    from glob import glob

    main(glob(sys.argv[1]))
