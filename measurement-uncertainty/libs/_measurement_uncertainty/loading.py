import os
import typing

import numpy as np
import pandas as pd

TRACK_PREFIXES = ('lp', 'rp', 'lm', 'rm')


def load_csv(
        csv_path: str,
        min_track_threshold: int
) -> typing.List[dict]:
    """
    Get a flat list of tracks where each row entry is a single track instead
    of a group of tracks for various limbs and populated with additional
    trackway information parsed from the CSV filename

    :param csv_path:
    :param min_track_threshold:
        The minimum number of tracks allowed within a trackway or the tracks
        for that trackway will not be included in the returned result
    :return:
        A list of dictionaries where each entry is a track loaded from a
        tracksim CSV file
    """

    df = pd.read_csv(csv_path)
    trackway_data = path_to_trackway_data(csv_path)

    tracks = [
        {**track, **trackway_data, **get_relative_uncertainties(track)}
        for index, row in df.iterrows()
        for track in to_tracks_list(index, row)
    ]

    pes_tracks = [t for t in tracks if t['is_pes']]
    return tracks if len(pes_tracks) >= min_track_threshold else []


def path_to_trackway_data(csv_path: str) -> dict:
    """
    Parses the trackway information from a tracksim formatted CSV source file
    path and returns that information as a dictionary

    :param csv_path:
        Path to a tracksim CSV file
    :return:
        A dictionary containing trackway information for the specified tracksim
        CSV file path
    """

    trackway_name = csv_path.split(os.path.sep)[-1].split('.')[0]
    parts = trackway_name.split('-')

    return dict(
        trackway=trackway_name,
        site=parts[0],
        level=parts[1],
        year=parts[2],
        sector='-'.join(parts[3:-2]),
        number=parts[-1]
    )


def get_relative_uncertainties(track: dict) -> dict:
    """
    Calculates relative uncertainties in track width and length as well as
    an L2 (Euclidean) combined value of the two uncertainties

    :param track:
        Data for a track, which must contain width and length information
        with associated uncertainties
    :return:
        Dictionary containing relative uncertainty data for the given track
    """

    def compute_relative_uncertainty(property_name: str) -> float:
        value = abs(track[property_name])
        uncertainty = track['d{}'.format(property_name)]
        return (uncertainty / value) if (value > 0) else 0

    dw_relative = compute_relative_uncertainty('w')
    dl_relative = compute_relative_uncertainty('l')

    return dict(
        dw_relative=dw_relative,
        dl_relative=dl_relative,
        max_relative=max(dw_relative, dl_relative)
    )


def to_tracks_list(index: int, row: pd.Series) -> typing.List[dict]:
    """
    Converts a tracksim CSV row from a group of tracks for each limb into a
    list of tracks for each limb. If one or more tracks are non-existent in the
    row, no data is returned for them.

    :param index:
        Row number within the CSV source file
    :param row:
        Row data for the group of tracks at the specified index
    :return:
        A list of zero or more dictionaries, where each dictionary contains the
        information for a single track extracted from the source row data
    """

    return list(filter(
        lambda track: (track is not None),
        [extract_track_data(prefix, row, index) for prefix in TRACK_PREFIXES]
    ))


def extract_track_data(
        prefix: str,
        row: pd.Series,
        index: int = 0
) -> typing.Union[dict, None]:
    """
    Extracts the track data for a single track of the specified limb prefix
    from the given row data

    :param prefix:
        A limb identifier, which is one of lp, rp, lm or rm
    :param row:
        The row from the tracksim CSV file in which the track will be extracted
    :param index:
        Index of the row within the tracksim CSV source file
    :return:
        A dictionary containing the data for the specified track if such a
        track exists or None if no track exists for the given limb within
        the row
    """

    if not has_track_data(prefix, row):
        return None

    key_prefix = '{}_'.format(prefix)

    data = dict([
        (key[len(key_prefix):], value)
        for key, value in row.to_dict().items()
        if key.startswith(key_prefix)
    ])
    data['limb'] = prefix
    data['is_left'] = bool(prefix[0] == 'l')
    data['is_pes'] = bool(prefix[1] == 'p')
    data['limb_index'] = index

    return data


def has_track_data(prefix: str, row: pd.Series) -> bool:
    """
    Determines whether or not a track exists for the specified limb within the
    given row

    :param prefix:
        A limb identifier, which is one of lp, rp, lm or rm
    :param row:
        Row from a tracksim-CSV-loaded DataFrame
    :return:
        Whether or not a track exists for the specified limb in the row
    """

    def is_nan(value) -> bool:
        try:
            return np.isnan(value)
        except TypeError:
            return False

    def has_data(property_name) -> bool:
        value = row[as_column_name(prefix, property_name)]
        return (value is not None) and (not is_nan(value))

    return bool(has_data('name') or has_data('uid'))


def as_column_name(prefix: str, property_name: str) -> str:
    """
    Converts a limb identifier prefix, e.g lp or rm, and a given property name
    to the equivalent column name specified in the tracksim CSV format

    :param prefix:
        A limb identifier, which is one of lp, rp, lm or rm
    :param property_name:
        The name of a property to be converted into a limb-specific column name
        for tracksim CSV format IO
    :return:
        The limb-specific column name for the given property name according to
        the tracksim CSV format
    """

    return '{}_{}'.format(prefix, property_name)
