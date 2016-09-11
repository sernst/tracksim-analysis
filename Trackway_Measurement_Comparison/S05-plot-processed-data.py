import locale

import cauldron as cd
import numpy as np
import plotly.graph_objs as go

locale.setlocale(locale.LC_ALL, ('en_US', 'utf8'))


def make_layout(
        metadata,
        title,
        fixed=False,
        x_axis=None,
        y_axis=None,
        **kwargs
):
    if not y_axis:
        y_axis = dict()
    y_axis.setdefault('title', 'Frequency')
    y_axis.setdefault('autorange', True)
    y_axis = go.YAxis(**y_axis)

    if not x_axis:
        x_axis = dict()
    x_axis.setdefault('title', 'Deviation (%)')
    x_axis = go.XAxis(**x_axis)

    if fixed:
        x_axis['range'] = [
            100.0 * metadata['x_min'],
            100.0 * min(4.0, metadata['x_max'])]
        x_axis['autorange'] = False

    return go.Layout(title=title, xaxis=x_axis, yaxis=y_axis, **kwargs)


def create_remainder_trace(
        df_cdf,
        key,
        size_class,
        area_values,
        count_label,
        is_first
):
    """

    :param df_cdf:
    :param key:
    :param size_class:
    :param area_values:
    :param count_label:
    :param is_first:
    :return:
    """

    area_values = np.add(area_values, 100.0 * df_cdf['y'][:-1])
    scatter = go.Scatter(
        name='%s (%s)' % (size_class['name'], count_label),
        x=100.0 * df_cdf['x'][:-1],
        y=area_values,
        mode='lines',
        fill='tozeroy' if is_first else 'tonexty',
        line=go.Line(
            width=1.0,
            color=size_class['color']
        )
    )

    return area_values, scatter


def create_histogram_trace(df_histogram, key, size_class, count_label):
    """

    :param df_histogram:
    :param key:
    :param size_class:
    :param count_label:
    :return:
    """

    return go.Bar(
        name='%s (%s)' % (size_class['name'], count_label),
        x=100.0 * df_histogram['x'],
        y=df_histogram['y'],
        marker=go.Marker(color=size_class['color'])
    )


def plot_histogram(data: dict, key: str, label: str, is_log: bool = False):
    """

    :param data:
    :param key:
    :param label:
    :param is_log:
    :return:
    """

    traces = []

    for size_class in cd.shared.SIZE_CLASSES:
        size_data = data['sizes'][size_class['id']]
        track_count = int(size_data['count'])

        traces.append(create_histogram_trace(
            df_histogram=size_data['df_histogram'],
            key=key,
            size_class=size_class,
            count_label=locale.format('%d', track_count, grouping=True)
        ))

    title = 'Distribution of Track {} Deviations ({} Measurements)'.format(
        label,
        locale.format('%d', data['count'], grouping=True)
    )

    y_axis = {'title': 'Frequency'}
    if is_log:
        y_axis['title'] = 'Frequency (log)'
        y_axis['type'] = 'log'

    cd.display.plotly(
        data=traces,
        layout=make_layout(
            data,
            title=title,
            y_axis=y_axis,
            barmode='stack'
        )
    )


def plot_remainder(data: dict, key: str, label: str, is_log: bool = False):
    area_values = np.zeros(len(data['df_expected']['x']) - 1)
    traces = []

    for size_class in cd.shared.SIZE_CLASSES:
        size_data = data['sizes'][size_class['id']]
        track_count = int(size_data['count'])

        area_values, area_trace = create_remainder_trace(
            df_cdf=size_data['df_cdf'],
            key=key,
            area_values=area_values,
            is_first=cd.shared.SIZE_CLASSES.index(size_class) < 1,
            size_class=size_class,
            count_label=locale.format('%d', track_count, grouping=True)
        )
        traces.append(area_trace)

    title = 'Cumulative Remainder of {} Deviations ({} Tracks)'.format(
        label,
        locale.format('%d', data['count'], grouping=True)
    )

    y_axis = {'title': 'Population Remaining (%)'}
    if is_log:
        y_axis['title'] = 'Log {}'.format(y_axis['title'])
        y_axis['type'] = 'log'

    traces.append(go.Scatter(
        name='Normal Threshold',
        x=100.0 * data['df_expected']['x'],
        y=data['df_expected']['y'],
        mode='lines',
        line=go.Line(
            color='rgba(0, 0, 0, 0.75)',
            dash='dash',
            width=1.0
        )
    ))

    cd.display.plotly(
        data=traces,
        layout=make_layout(
            data,
            title=title,
            fixed=True,
            y_axis=y_axis
        )
    )

cd.shared.put(
    make_layout=make_layout,
    plot_histogram=plot_histogram,
    plot_remainder=plot_remainder
)
