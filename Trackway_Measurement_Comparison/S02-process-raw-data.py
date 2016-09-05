import json
import numpy as np
import os
import pandas as pd
import tables
import shutil
import cauldron as cd
import re
from scipy.stats import norm


DATA_DIR = os.path.realpath('data')
OUT_PATH = os.path.join(DATA_DIR, 'deviation.h5')
METADATA_FILE = os.path.join(DATA_DIR, 'deviation.metadata.json')

SIZE_CLASSES = [
    dict(
        id='t',
        index=0,
        range=(0, 0.25),
        name='Tiny',
        color='rgb(141,211,199)'
    ),
    dict(
        id='s',
        index=1,
        range=(0.25, 0.50),
        name='Small',
        color='rgb(188,128,189)'
    ),
    dict(
        id='m',
        index=2,
        range=(0.5, 0.75),
        name='Medium',
        color='rgb(190,186,218)'
    ),
    dict(
        id='l',
        index=3,
        range=(0.75, 100.0),
        name='Large',
        color='rgb(251,128,114)'
    )
]
cd.shared.SIZE_CLASSES = SIZE_CLASSES


def generate_data(name, df, key, bin_count):
    """
    Creates the data

    :param name:
        Name of the data file to be generated
    :param df:
        The source data frame on which to generate data
    :param key:
        The key for the data within the data frame
    :param bin_count:
        Number of bins to use when generating histogram data

    :return:
        A list of dictionaries containing structural information for the data
        saved to output data file
    """

    structure = []
    x_min = df[key].min()
    x_max = min(3.0, df[key].max())
    count = df.shape[0]
    x_values = np.linspace(x_min, x_max, 64)
    bins = np.linspace(x_min, x_max, int(bin_count))

    metadata = {
        'xMin': x_min,
        'xMax': x_max,
        'count': count,
        'size_counts': {},
        'bins': list(bins),
        'structure': structure
    }

    expected = []
    for x in x_values:
        expected.append(100.0 * (1.0 - (norm.cdf(x) - norm.cdf(-x))))
    expected_df = pd.DataFrame({
        'x': x_values,
        'y': expected
    })
    expected_df.to_hdf(OUT_PATH, '{}/expected'.format(name))

    # Calculate for all size classes, including an "all"
    sizes = [{'id': 'all'}] + SIZE_CLASSES

    for size_class in sizes:
        if 'index' in size_class:
            data_slice = df.query('sizeClass == {}'.format(size_class['index']))
        else:
            data_slice = df
        metadata['size_counts'][size_class['id']] = data_slice.shape[0]

        size_count = data_slice.shape[0]
        data_slice = data_slice.query('{} <= {}'.format(key, x_max))

        hist_values = np.histogram(a=data_slice[key].values, bins=bins)
        percent_values = hist_values[0] / count
        solo_percent_values = hist_values[0] / size_count

        hist_df = pd.DataFrame({
            'x': hist_values[1],
            'y': np.append(hist_values[0], [0]),
            'y_fractional': np.append(percent_values, [0]),
            'y_fractional_solo': np.append(solo_percent_values, [0])
        })

        structure.append({
            'key': '{}/{}/histogram'.format(name, size_class['id']),
            'columns': list(hist_df.columns.values)
        })

        hist_df.to_hdf(OUT_PATH, key=structure[-1]['key'], mode='a')

        hist_values = np.histogram(a=data_slice[key].values, bins=x_values)
        area_values = (size_count - np.cumsum(hist_values[0])) / count
        solo_area_values = (
           size_count - np.cumsum(hist_values[0])
        ) / size_count

        cdf_df = pd.DataFrame({
            'x': hist_values[1],
            'y': np.append(area_values, [0]),
            'y_solo': np.append(solo_area_values, [0])
        })

        structure.append({
            'key': '{}/{}/cumulative'.format(name, size_class['id']),
            'columns': list(cdf_df.columns.values)
        })

        cdf_df.to_hdf(OUT_PATH, key=structure[-1]['key'], mode='a')

    return metadata


def read_table(table_name, engine):
    """

    :param table_name:
    :param engine:
    :return:
    """

    def renaming_mapper(column_name):
        """

        :param column_name:
        :return:
        """

        if re.compile('^[^a-zA-Z_]+').match(column_name):
            return 'X{}'.format(column_name)
        return column_name

    df = pd.read_sql_table(table_name, engine)
    df.columns = map(renaming_mapper, list(df.columns))
    return df


def load_tracks_data():
    df = pd.merge(
        left=read_table('tracks', cd.shared.tracks_engine),
        right=read_table('tracks', cd.shared.analysis_engine),
        how='inner',
        on='uid',
        suffixes=('', '_analysis'))

    def size_class_mapper(track_width):
        """

        :param track_width:
        :return:
        """

        for size_class in SIZE_CLASSES:
            if track_width >= size_class['range'][1]:
                continue
            return size_class['index']
        return -1

    df['sizeClass'] = df['width'].map(size_class_mapper)
    return df


def initialize():
    """

    :return:
    """

    if os.path.exists(DATA_DIR):
        shutil.rmtree(DATA_DIR)
    os.makedirs(DATA_DIR)

    df = load_tracks_data()
    return df[['uid', 'site', 'width', 'sizeClass']]


def write_structure_file(structure):
    """

    :param structure:
    :return:
    """

    with open(METADATA_FILE, 'w') as f:
        f.write(json.dumps(
            obj=structure,
            separators=(',', ': '),
            indent=2,
            sort_keys=True
        ))


def validate():
    """

    :return:
    """

    try:
        data = tables.open_file(OUT_PATH)
        data.close()
    except Exception as err:
        print('[ERROR] Failed to open generated data file')
        raise err

    # Test loading one of the dataframes
    try:
        pd.read_hdf(OUT_PATH, '/stride/all/cumulative')
    except Exception as err:
        print('[ERROR] Failed to load dataframe from file')
        raise err


def get_analysis_data(
        analyzer_name: str,
        filename: str,
        renames=None
):
    """ Using the analyzer class and CSV filename, return a Pandas DataFrame
        containing that data.

    :param analyzer_name:
    :param filename:
    :param renames:
        A dictionary containing columns to rename. The old column names are the
        keys and the new column names the values.

    :return:
    """

    def read_csv(csv_path, encoding):
        """
        :param csv_path:
        :param encoding:
        :return:
        """

        try:
            return pd.read_csv(csv_path, encoding=encoding)
        except:
            return None

    def replace_mapper(column_name):
        """

        :param column_name:
        :return:
        """

        if not renames or column_name not in renames:
            return column_name
        return renames[column_name]

    path = os.path.join(
        os.path.expanduser('~'),
        'Dropbox',
        'A16',
        'Analysis',
        analyzer_name,
        filename
    )

    df = None
    for e in ['utf8', 'mac_roman']:
        df = read_csv(path, e)

    df.columns = map(replace_mapper, list(df.columns))
    return df


def run():
    """

    :return:
    """

    tracks = initialize()
    structure = {}

    # --- TRACK LENGTH & WIDTH ---#
    df = get_analysis_data(
        'ComparisonAnalyzer',
        'Length-Width-Deviations.csv',
        renames={
            'Width Deviation': 'widthDeviation',
            'Length Deviation': 'lengthDeviation',
            'Fingerprint': 'fingerprint',
            'UID': 'uid'
        })

    df = pd.merge(df, tracks, left_on='uid', right_on='uid')

    structure['width'] = generate_data(  # Track Width
        name='width',
        key='widthDeviation',
        df=df.query('widthDeviation >= 0.0'),
        bin_count=10.0)

    structure['length'] = generate_data(  # Track Length
        name='length',
        key='lengthDeviation',
        df=df.query('lengthDeviation >= 0.0'),
        bin_count=10.0)

    # --- STRIDE LENGTH ---#
    df = get_analysis_data(
        'ValidationAnalyzer',
        'Stride-Length-Deviations.csv',
        renames={'UID': 'uid'}
    )

    df = pd.merge(df, tracks, on='uid')

    structure['stride'] = generate_data('stride', df, 'Deviation', 10.0)

    # --- PACE LENGTH ---#
    df = get_analysis_data(
        'ValidationAnalyzer',
        'Pace-Length-Deviations.csv',
        renames={'UID': 'uid'}
    )

    df = pd.merge(df, tracks, on='uid')

    structure['pace'] = generate_data('pace', df, 'Deviation', 10.0)

    write_structure_file(structure)

    validate()

run()
cd.shared.put(
    load_tracks_data=load_tracks_data
)
