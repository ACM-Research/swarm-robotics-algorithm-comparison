from pandas import DataFrame
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler


def density(positions, eps, min_samples):
    """
    Estimate the density of resources using DBSCAN.

    :param positions: a 2D array of coordinate components (aka an array of
    positions).
    :param eps: the size of a "neighborhood"; increase to make
    clustering more lenient.
    :param min_samples: the minimum number of other
    points in a point's neighborhood required for it to be considered a "core
    point".
    :return: a tuple consisting of the number of clusters found and
    the number of "noise points" that weren't clustered.
    """
    # standardize positions by removing the mean and scaling to unit variance.
    scaled_positions = StandardScaler().fit_transform(positions)
    labels = DBSCAN(eps=eps, min_samples=min_samples).fit_predict(
        scaled_positions)

    # count estimated clusters, but ignore non-clustered points
    clusters = len(set(labels)) - (1 if -1 in labels else 0)
    # also extract non-clustered points
    noise = list(labels).count(-1)
    return clusters, noise


def density_over_time(simulation, eps, min_samples=5):
    """
    :param simulation: a DataFrame of x,y,z coordinates indexed by timestamp
    :return: a DataFrame with columns [timestamp, clusters, noise]
    """
    # return simulation.groupby('timestamp').apply(
    #     lambda moment: Series([moment.timestamp]) + Series(
    #         density(array(moment), eps, min_samples),
    #         index=['clusters', 'noise']))
    return DataFrame.from_records(
        ((float(t), *density(moment, eps, min_samples)) for t, moment in
         simulation.groupby('timestamp')),
        columns=['timestamp', 'clusters', 'noise'])
