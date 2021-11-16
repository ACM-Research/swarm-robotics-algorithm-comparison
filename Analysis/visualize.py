import sys

import matplotlib.pyplot as plt
import seaborn
from pandas import concat

from density import density_over_time
from parse import parse, parse_name
from playback import coordinates_by_timestamp


def main(log_files):
    recordings = [parse(file) for file in log_files]
    playbacks = [coordinates_by_timestamp(recording) for recording in
                 recordings]
    densities = concat([density_over_time(playback, eps=.1,
                                          min_samples=3).assign(
        **parse_name(log_files[i])) for i, playback in enumerate(playbacks)],
        join='inner', ignore_index=True)

    # extra processing
    densities['scaled noise'] = densities['noise'] / densities['resources']
    densities['run'] = densities.apply(
        lambda sample: '{robots} robots, {resources} resources'.format(
            robots=sample['robots'],
            resources=
            sample[
                'resources']),
        axis=1)

    # densities.set_index(['simulation', 'run', 'map', 'algorithm', 'timestamp'])

    seaborn.set_theme()

    seaborn.relplot(data=densities[densities['scaled noise'] <= 1.0],
                    kind='line', x='timestamp',
                    y='scaled noise',
                    hue='algorithm', units='simulation', estimator=None,
                    col='map', style='run').set(
        ylabel='Proportion of Non-Clustered Points', xlabel='Time (s)')
    # seaborn.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))

    plt.show()


if __name__ == '__main__':
    main(sys.argv[1:])
