import typing
import pandas as pd
from scipy.interpolate import interp1d
import measurement_stats as mstats

InterpPoints = typing.List[typing.Tuple[float, float, float]]


def fill_interpolates(count: int, interpolates: InterpPoints) -> InterpPoints:
    """
    Create a fully populated list of keyframe interpolates for the midline
    offsets, which includes filling in missing keyframes at the beginning and
    end of the specified list of interpolation points if they do not exist.

    The resulting list is also sorted to make sure that the keyframes are
    monotonically sorted with respect to track index.

    :param count:
        The number of tracks in the generated trackway
    :param interpolates:
        The raw list of interpolation keyframes for the midline offsets. If
        no values are provided, a default list will be created instead.
    :return:
    """

    if not interpolates:
        return [(1, 0.5, 0.00001), (count, 0.5, 0.00001)]

    interp_values = sorted(list(interpolates), key=lambda x: x[0])

    first_value = interp_values[0]
    if first_value[0] > 1:
        interp_values.insert(0, (1, first_value[1], first_value[2]))

    last_value = interp_values[-1]
    if last_value[0] < count:
        interp_values.append((count, last_value[1], last_value[2]))

    return interp_values


def get_midline_offsets(
        count: int,
        interpolate_keyframes: InterpPoints
) -> typing.List[mstats.ValueUncertainty]:
    """

    :param count:
    :param interpolate_keyframes:
    :return:
    """

    interp_values = fill_interpolates(count, interpolate_keyframes)
    x_values = [interp[0] for interp in interp_values]
    y_values = [interp[1] for interp in interp_values]
    uncertainties = [interp[2] for interp in interp_values]

    values_interpolator = interp1d(x_values, y_values, 'linear')
    uncertainties_interpolator = interp1d(x_values, uncertainties, 'linear')

    return mstats.values.join(
        list(values_interpolator(list(range(1, count + 1)))),
        list(uncertainties_interpolator(list(range(1, count + 1)))),
    )


def make_track_entry(
        index: int,
        midline_offset: mstats.ValueUncertainty
) -> dict:
    """
    Creates a dictionary containing the track information for the track at
    the specified index and offset the specified distance away from the
    midline for the trackway

    :param index:
        The 1-indexed index for the track in the trackway
    :param midline_offset:
        The distance away from the trackway's midline where the track will
        be placed.
    :return:
        A dictionary containing the information for the created track
    """

    is_left = (index & 1)

    sign = 1 if is_left else -1

    return dict(
        index=index,
        curvePosition=float(index),
        left=is_left,
        pes=True,
        x=float(index),
        y=sign * midline_offset.value,
        dy=midline_offset.uncertainty
    )


def calculate_gauge(
        track: dict,
        tracks: typing.List[dict]
) -> mstats.ValueUncertainty:
    """

    :param track:
    :param tracks:
    :return:
    """

    index = tracks.index(track)
    last_index = len(tracks) - 1
    before = tracks[index - 1] if index > 0 else tracks[index + 1]
    after = tracks[index + 1] if index < last_index else tracks[index - 1]

    y = mstats.ValueUncertainty(track['y'], track['dy'])
    y_before = mstats.ValueUncertainty(before['y'], before['dy'])
    y_after = mstats.ValueUncertainty(after['y'], after['dy'])

    gauge = (
        abs(y) +
        abs(y_before + y_after) / 2
    )  # type: mstats.ValueUncertainty

    return gauge


def create(
        count: int,
        *midline_offset_interpolates: InterpPoints
) -> pd.DataFrame:
    """
    Generates trackway data under the specified conditions for use in example
    analyses

    :param count:
        The number of tracks to include in the trackway
    :param midline_offset_interpolates:
        Point tuples representing interpolation keyframe values at various
        positions along the trackway. The x value of the point is the index
        of the track where the keyframe will reside. The y value is the
        distance from the trackway midline that the track at that index will
        be assigned. Cubic interpolation is used to fill in any values not
        specified in this list
    :return:
        A data frame containing the generated track data for the computed
        trackway
    """

    midline_offsets = get_midline_offsets(count, midline_offset_interpolates)

    tracks = [
        make_track_entry(index + 1, midline_offsets[index])
        for index in range(count)
    ]

    df = pd.DataFrame(tracks)

    gauges = [calculate_gauge(track, tracks) for track in tracks]
    df['simpleGauge'] = [g.value for g in gauges]
    df['simpleGaugeUnc'] = [g.uncertainty for g in gauges]

    return df
