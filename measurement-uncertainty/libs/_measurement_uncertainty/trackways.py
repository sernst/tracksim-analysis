from collections import OrderedDict

import pandas as pd


def for_each(
        callback,
        tracks_df: pd.DataFrame,
        **kwargs
) -> OrderedDict:
    """

    :param callback:
    :param tracks_df:
    :return:
    """

    trackway_names = list(tracks_df['trackway'].unique())

    def on_trackway(name: str):
        progress = (1 + trackway_names.index(name)) / len(trackway_names)
        return on(callback, name, tracks_df, progress=progress, **kwargs)

    return OrderedDict([
        (name, on_trackway(name))
        for name in tracks_df['trackway'].unique()
    ])


def on(
        callback,
        trackway_name: str,
        tracks_df: pd.DataFrame,
        progress: float,
        **kwargs
):
    """

    :param callback:
    :param trackway_name:
    :param tracks_df:
    :param progress:
    :return:
    """

    slice_df = tracks_df[tracks_df['trackway'] == trackway_name]
    return callback(trackway_name, slice_df, progress=progress, **kwargs)
