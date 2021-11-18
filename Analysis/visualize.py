import sys
from time import perf_counter

import matplotlib.pyplot as plt
import seaborn
from joblib import delayed, Parallel
from pandas import concat, DataFrame

from density import density_over_time
from parse import parse, parse_name
from playback import coordinates_by_timestamp


def main(log_files):
    program_start = perf_counter()
    start = perf_counter()
    # recordings = [parse(file) for file in log_files]
    recordings = Parallel(n_jobs=-1)(delayed(parse)(file) for file in log_files)
    print(f'Parsed recordings in {perf_counter() - start:.3f}s')
    # recordings = pool.map(parse, log_files)

    start = perf_counter()
    # playbacks = [coordinates_by_timestamp(recording) for recording in recordings]
    playbacks = Parallel(n_jobs=-1, verbose=10)(
        delayed(coordinates_by_timestamp)(recording) for recording in
        recordings)
    print(f'Played back recordings in {perf_counter() - start:.3f}s')
    # playbacks = pool.map(coordinates_by_timestamp, recordings)

    start = perf_counter()
    all_densities = Parallel(n_jobs=-1, verbose=10)(
        delayed(density_over_time)(playback, eps=.1, min_samples=3) for playback
        in playbacks)
    print(f'Calculated densities in {perf_counter() - start:.3f}s')

    start = perf_counter()
    densities = concat(Parallel(n_jobs=-1, verbose=10)(
        delayed(DataFrame.assign)(density, **parse_name(log_files[i])) for
        i, density in enumerate(all_densities)), ignore_index=True)
    print(f'Added metadata to dataframe in {perf_counter() - start:.3f}s')

    # extra processing
    start = perf_counter()
    densities['scaled noise'] = densities['noise'] / densities['resources']
    densities['run'] = densities.apply(
        lambda sample: '{robots} robots, {resources} resources'.format(
            robots=sample['robots'], resources=sample['resources']), axis=1)
    print(f'Processed densities in {perf_counter() - start:.3f}s')

    start = perf_counter()
    plt.figure(figsize=(14, 6), dpi=300)
    seaborn.set_theme()

    seaborn.relplot(data=densities[densities['scaled noise'] <= 1.0],
                    kind='line', x='timestamp',
                    y='scaled noise',
                    hue='algorithm', units='simulation', estimator=None,
                    col='map', style='run').set(
        ylabel='Proportion of Non-Clustered Points', xlabel='Time (s)')
    # seaborn.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))

    print(f'Created visualization in {perf_counter() - start:.3f}s')
    plt.show()
    print(f'{sys.argv[0]} completed in {perf_counter() - program_start:.3f}s')


if __name__ == '__main__':
    from glob import glob

    main(glob(sys.argv[1]))
