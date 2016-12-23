import typing
import math

import cauldron as cd
import numpy as np
import pandas as pd
from bokeh.charts import Histogram

df_tracks = cd.shared.df_tracks.copy()  # type: pd.DataFrame
df_out = cd.shared.df_out  # type: pd.DataFrame
csv_columns = cd.shared.csv_columns  # type: pd.DataFrame

# Cadence rotation values have a -90 degree offset caused by the
# 3D coordinate system in which it was created
df_tracks['abs_rotation'] = 90 + df_tracks['rotation']


def get_position(track: pd.Series) -> tuple:
    """ Convert to a 2D RH coordinate system: z -> x and x -> y"""

    return track['z'], track['x']


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


def get_stride_angle(track: pd.Series) -> typing.Union[float, None]:
    """
    Calculates the stride angle for the given track. If the track is
    isolated and so no such stride angle exists, a value of None is
    returned instead.

    :param track:
        The track for which the stride angle should be calculated.
    :return:
        The stride angle for the given track or None
    """

    track_next = get_next_track(track)
    if track_next is None:
        return None

    position_a = get_position(track)
    position_b = get_position(track_next)

    x = position_b[0] - position_a[0]
    y = position_b[1] - position_a[1]

    return round(90 + math.degrees(math.atan2(y, x)))

df_tracks['stride_angle'] = [
    get_stride_angle(r)
    for _, r in df_tracks.iterrows()
]


def fill_end_tracks(track: pd.Series) -> typing.Union[float, None]:
    """
    Populate stride angles for tracks at the end of the series and have no
    next track. The A16 catalog convention here is to use the stride angle of
    the previous track in place of one for the final track. If the specified
    track has a next track, its existing stride angle is returned instead,
    which makes this safe to run on all tracks, not just ones at the
    end of a track series.

    :param track:
        The track on which to lookup the stride angle
    :return:
        The stride angle for the track. This will be either its existing value
        or, for tracks at the end of a track series, the value of its
        previous track. If the track is isolated and has not previous or next
        track, a value of None is returned instead.
    """

    if not np.isnan(track['stride_angle']):
        return track['stride_angle']

    uid = track['uid']
    df_previous = df_tracks[uid == df_tracks['next']]

    if df_previous.shape[0] != 1:
        return None

    previous_track = df_previous.iloc[0]
    return previous_track['stride_angle']


df_tracks['stride_angle'] = [
    fill_end_tracks(r)
    for _, r in df_tracks.iterrows()
]


cd.display.markdown(
    """
    # Track Rotation

    The difficulty in exporting rotation angles is that the Cadence database
    stores absolute angles while the catalog stores relative angles that use
    the stride line as the reference axis. In addition, the sign of the catalog
    rotations are different depending on whether the track is a left or right
    foot. A positive catalog rotation always indicates an outward rotation
    relative to the reference stride line axis.

    The conversion from absolute coordinates first requires calculating the
    absolute angles of the stride lines. These angles are computed from the
    Cadence position values of the track center and its next track if such a
    track exists. Tracks without a next value are assigned NaN values for the
    stride angle.

    To check that the stride angles were calculated properly we plot a
    histogram of the difference of the stride angle and the Cadence rotation
    value for the track. We expect differences in these values, but we expect
    the majority of them to be less than 90 degrees for anatomical reasons.
    The following histogram confirms that we've properly calculated the stride
    angles.
    """
)


def compute_delta(track: pd.Series) -> float:
    """
    Calculates the shortest angular delta between the Cadence rotation and
    the stride line angle for the specified track entry.

    :param track:
        A track row from the df_tracks DataFrame
    :return:
        The smallest angle, in degrees, between the Cadence rotation angle
        and the stride line angle for the given track.
    """

    delta = track['abs_rotation'] - track['stride_angle']
    return abs(delta if delta < 180 else (360 - delta))

df_tracks['delta'] = df_tracks.apply(compute_delta, axis=1)
cd.display.bokeh(Histogram(
    data=df_tracks.dropna(subset=['delta']),
    values='delta',
    xlabel='Angular Difference (degrees)'
))

cd.display.markdown(
    """
    These rotation differences are almost what is needed for the local rotation
    values. What remains is taking into account the different signs for the
    left and right body positions. Accounting for this yields the histogram of
    local rotations:
    """
)


def get_local_rotation(track: pd.Series) -> typing.Union[float, None]:
    if track['delta'] is None:
        return None

    def constrain_angle(a: float) -> float:
        if abs(a) < 180:
            return a
        elif a < 0:
            return 360 + a

        return a - 360

    stride_angle = constrain_angle(track['stride_angle'])
    cadence_angle = constrain_angle(track['abs_rotation'])

    if track['left']:
        sign = 1 if cadence_angle > stride_angle else -1
    else:
        sign = 1 if stride_angle > cadence_angle else -1

    return sign * track['delta']

df_tracks['local_rotation'] = [
    get_local_rotation(r)
    for _, r in df_tracks.iterrows()
]

cd.display.bokeh(Histogram(
    data=df_tracks.dropna(subset=['local_rotation']),
    values='local_rotation',
    xlabel='Local Rotations (degrees)'
))

cd.display.markdown(
    """
    A strong positive bias in the values is good validation as well given the
    known anatomical preference for these Sauropods to walk with their feet
    pointed outward.

    Because catalog rotations require defining a stride line axis for
    reference, the local rotation values for isolated tracks cannot be
    calculated. The following tracks have no rotation values to export for
    this reason:
    """
)

cd.display.table(df_tracks[df_tracks['stride_angle'].isnull()])

GUESS_THRESHOLD = 180 * 0.12


def create(**kwargs) -> dict:
    out = dict([
        (column.name, None)
        for column in (csv_columns[29:33] + csv_columns[39:43])
    ])
    out.update(**kwargs)
    return out


def get_column_indices(track: pd.Series) -> tuple:
    if track['pes']:
        return (29, 30) if track['left'] else (31, 32)

    return (39, 40) if track['left'] else (41, 42)


def to_rotation(track: pd.Series) -> dict:
    is_guess = (track['rotationUncertainty'] >= GUESS_THRESHOLD)
    indices = get_column_indices(track)
    index = indices[1] if is_guess else indices[0]

    return create(
        uid=track['uid'],
        **{csv_columns[index].name: track['local_rotation']}
    )

for key in create().keys():
    df_out = df_out.drop([key], axis=1, errors='ignore')

df = pd.DataFrame([to_rotation(r) for _, r in df_tracks.iterrows()])
df_out = pd.merge(left=df_out, right=df, how='inner', on='uid')

cd.shared.df_out = df_out
