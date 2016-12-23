import typing

import cauldron as cd
import pandas as pd
from bokeh.plotting import Figure

df_tracks = cd.shared.df_tracks  # type: pd.DataFrame
df_out = cd.shared.df_out  # type: pd.DataFrame
csv_columns = cd.shared.csv_columns  # type: pd.DataFrame

GUESS_THRESHOLD = 0.2


def create(**kwargs) -> dict:
    pairs = [
        (csv_columns[index].name, None)
        for index in (43, 44, 45, 58, 59, 60)
    ]

    return dict(pairs, **kwargs)


def get_next_track(track: pd.Series) -> typing.Union[None, pd.Series]:
    """
    Returns the track row for the next specified track in the series for the
    given track. A value of None is returned if no such track exists.
    :param track:
        The previous track of the track to be returned
    :return:
        The track that follows the given track in the trackway series
    """

    if not track['next']:
        return None

    return df_tracks.query('uid == "{}"'.format(track['next'])).iloc[0]


def get_tracks_between(start_track: pd.Series, end_track: pd.Series) -> list:
    out = [start_track]

    while out[-1] is not None and out[-1]['uid'] != end_track['uid']:
        out.append(get_next_track(out[-1]))

    return list(filter(
        lambda t: (t is not None and t['uid'] != end_track['uid']),
        out
    ))


def get_stride_factor(track: pd.Series) -> int:
    def match(track_data: pd.Series, left: bool, pes: bool) -> int:
        yes = (track_data['left'] == left) and (track_data['pes'] == pes)
        return (1 if yes else 0)

    next_track = df_tracks.query('uid == "{}"'.format(track['next'])).iloc[0]
    delta = int(next_track['number']) - int(track['number'])

    between = get_tracks_between(track, next_track)
    counts = [
        sum([match(t, True, True) for t in between]),
        sum([match(t, False, True) for t in between]),
        sum([match(t, True, False) for t in between]),
        sum([match(t, False, False) for t in between])
    ]

    return max(1, delta, *counts)


def to_stride(track: pd.Series) -> dict:
    out = create(uid=track['uid'])

    if not track['strideLength']:
        return out

    indices = [43, 44, 45] if track['pes'] else [58, 59, 60]
    is_guess = (0.2 <= (track['strideLengthUnc'] / track['strideLength']))
    index = indices[1] if is_guess else indices[0]
    stride_length = 0.01 * round(100 * track['strideLength'])

    out.update({
        csv_columns[index].name: stride_length,
        csv_columns[indices[-1]].name: get_stride_factor(track)
    })
    return out


df = pd.DataFrame([to_stride(t) for _, t in df_tracks.iterrows()])

for key in create().keys():
    df_out = df_out.drop([key], axis=1, errors='ignore')
df_out = pd.merge(df_out, df, on='uid')

cd.display.markdown(
    """
    # Stride Length

    Stride lengths are calculated as part of the Cadence analysis process and
    are stored in the analysis database. To export them, the stride length
    uncertainties were used to determine whether the value should reside in
    the guess column or not.

    Stride factors add a complication as they were not dealt within
    Cadence. The trackway curve projection algorithm results were used to
    determine stride factors by looking at the tracks found between each track
    and the subsequent track in the series. The presence of multiple tracks for
    another foot in the trackway indicates a stride factor greater than 1.
    The results are plotted below. To improve the plot value, the stride length
    ratio was plotted instead of the stride length. The stride length ratio is
    the stride length normalized by the width of the foot. This reduces value
    spread due to size of the animal, which would be an undesirable artificat
    in this plot.
    """
)

figure = Figure(
    title='Stride Length Ratio versus Stride Factors',
    x_axis_label='Stride Factor (#)',
    y_axis_label='Stride Length Ratio (#)'
)


def add_scatter(pes: bool, color: str, guess_color: str):
    indices = [43, 44, 45] if pes else [58, 59, 60]
    names = [csv_columns[i].name for i in indices]

    df_slice = pd.merge(
        df_out[df[names[0]].notnull()],
        df_tracks[['uid', 'width']],
        how='left',
        on='uid'
    )

    figure.scatter(
        df_slice[names[-1]],
        df_slice[names[0]] / df_slice['width'],
        color=color,
        legend='Pes' if pes else 'Manus'
    )

    df_slice = pd.merge(
        df_out[df[names[1]].notnull()],
        df_tracks[['uid', 'width']],
        how='left',
        on='uid'
    )

    figure.scatter(
        df_slice[names[-1]],
        df_slice[names[1]],
        color=guess_color,
        legend='{} Guess'.format('Pes' if pes else 'Manus')
    )

add_scatter(True, 'blue', 'purple')
add_scatter(False, 'red', 'orange')
figure.legend.location = 'bottom_right'
cd.display.bokeh(figure)

cd.display.markdown(
    """
    There are no obvious outliers in the data. We don't see any excessively
    large stride length ratios for low stride factors, which is reassuring.
    There is an amount of overlap between the value ranges for different
    stride factors, but the resolution of those would require a deeper
    analysis. Stride factor is and should remain an interpreted and imperfect
    value within the catalog.
    """
)

cd.shared.df_out = df_out
