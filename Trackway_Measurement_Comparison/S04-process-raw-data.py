import os

import cauldron as cd
import numpy as np
import pandas as pd
from scipy.stats import norm
import measurement_stats as mstats

SIZE_CLASSES = cd.shared.SIZE_CLASSES


def generate_data_for_size(df, key, size_class, totals):
    results = dict()

    if 'index' in size_class:
        df_size = df.query('size_class == {}'.format(size_class['index']))
    else:
        df_size = df

    results['count'] = df_size.shape[0]

    count = df_size.shape[0]
    df_size = df_size.query('{} <= {}'.format(key, totals['x_max']))

    hist_values = np.histogram(a=df_size[key].values, bins=totals['bins'])
    percent_values = hist_values[0] / totals['count']
    solo_percent_values = hist_values[0] / count

    results['df_histogram'] = pd.DataFrame({
        'x': hist_values[1],
        'y': np.append(hist_values[0], [0]),
        'y_fractional': np.append(percent_values, [0]),
        'y_fractional_solo': np.append(solo_percent_values, [0])
    })

    hist_values = np.histogram(
        a=df_size[key].values,
        bins=totals['x_values']
    )

    area_values = (count - np.cumsum(hist_values[0])) / totals['count']
    solo_area_values = (count - np.cumsum(hist_values[0])) / count

    results['df_cdf'] = pd.DataFrame({
        'x': hist_values[1],
        'y': np.append(area_values, [0]),
        'y_solo': np.append(solo_area_values, [0])
    })

    return results


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

    x_min = df[key].min()
    x_max = min(3.0, df[key].max())
    count = df.shape[0]
    x_values = np.linspace(x_min, x_max, 64)
    bins = np.linspace(x_min, x_max, int(bin_count))

    results = {
        'x_values': x_values,
        'x_min': x_min,
        'x_max': x_max,
        'count': count,
        'sizes': {},
        'bins': list(bins)
    }

    expected = []
    for x in x_values:
        expected.append(100.0 * (1.0 - (norm.cdf(x) - norm.cdf(-x))))

    df_expected = pd.DataFrame({'x': x_values, 'y': expected})
    results['df_expected'] = df_expected

    for size_class in ([{'id': 'all'}] + SIZE_CLASSES):
        # Calculate for all size classes, including an "all"
        entry = generate_data_for_size(df, key, size_class, results)
        results['sizes'][size_class['id']] = entry

    return results


def get_analyzer_results(
        analyzer_name: str,
        filename: str,
        renames=None
):
    """
    Using the analyzer class and CSV filename, return a Pandas DataFrame
    containing that data.

    :param analyzer_name:
    :param filename:
    :param renames:
        A dictionary containing columns to rename. The old column names are the
        keys and the new column names the values.

    :return:
    """

    def replace_mapper(column_name):
        if not renames or column_name not in renames:
            return column_name
        return renames[column_name]

    def read_csv(csv_path, encoding):
        try:
            df = pd.read_csv(csv_path, encoding=encoding)
            df.columns = map(replace_mapper, list(df.columns))
            return df
        except:
            return None

    path = os.path.join(
        cd.shared.ROOT_PATH,
        'Analysis',
        analyzer_name,
        filename
    )

    for e in ['utf8', 'mac_roman']:
        df = read_csv(path, e)
        if df is not None:
            return df


def closest_value(source, target):
    """

    :param source:
    :param target:
    :return:
    """

    out = 1e6
    for value in source:
        if abs(value - target) < abs(out - target):
            out = value
    return out


def cdr_values_at(measurement_data, x_values):
    """

    :param measurement_data:
    :param x_values:
    :return:
    """

    df_cdf = measurement_data['sizes']['all']['df_cdf']

    out = dict()

    for x_target in x_values:
        x = closest_value(df_cdf['x'], x_target)
        y = df_cdf[df_cdf['x'] == x]['y'].values[0]
        label = '{:0.1f}'.format(
            mstats.value.round_to_order(100 * (1 - y), -1)
        )
        out[x_target] = dict(
            x=x,
            x_target=x_target,
            y=y,
            label=label
        )

    return out


cd.shared.put(
    generate_data=generate_data,
    get_analyzer_results=get_analyzer_results,
    closest_value=closest_value,
    cdr_values_at=cdr_values_at
)
