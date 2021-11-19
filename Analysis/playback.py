from pandas import DataFrame


def verify(updates: DataFrame) -> bool:
    counts = updates.groupby('timestamp')['id'].count()
    return counts.eq(counts.iloc[0]).all()


def coordinates_by_timestamp(updates):
    relevent_logs = updates[updates['event'] == 'TICK']
    moments = relevent_logs[['timestamp', 'x', 'y', 'z']].set_index('timestamp')
    return moments
