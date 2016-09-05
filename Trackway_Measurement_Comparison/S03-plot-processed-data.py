import functools
import json
import locale
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import os
import cauldron as cd

locale.setlocale(locale.LC_ALL, ('en_US', 'utf8'))

DATA_DIR = os.path.realpath('data')
OUT_PATH = os.path.join(DATA_DIR, 'deviation.h5')
METADATA_FILE = os.path.join(DATA_DIR, 'deviation.metadata.json')


def _get_layout(
        metadata,
        title,
        fixed=False,
        x_axis=None,
        y_axis=None,
        **kwargs
):
    if not x_axis:
        x_axis = {}
    x_axis.setdefault('title', 'Deviation (%)')

    if not y_axis:
        y_axis = {}
    y_axis.setdefault('title', 'Frequency')
    y_axis.setdefault('autorange', True)

    x_axis = go.XAxis(**x_axis)
    y_axis = go.YAxis(**y_axis)

    if fixed:
        x_axis['range'] = [
            100.0 * metadata['xMin'],
            100.0 * min(4.0, metadata['xMax'])]
        x_axis['autorange'] = False

    return go.Layout(title=title, xaxis=x_axis, yaxis=y_axis, **kwargs)


def _make_remainder(key, sizeClass, area_values, countLabel, isFirst):
    cdf_df = pd.read_hdf(OUT_PATH, key + 'cumulative')
    area_values = np.add(area_values, 100.0 * cdf_df['y'][:-1])
    scatter = go.Scatter(
        name='%s (%s)' % (sizeClass['name'], countLabel),
        x=100.0 * cdf_df['x'][:-1],
        y=area_values,
        mode='lines',
        fill='tozeroy' if isFirst else 'tonexty',
        line=go.Line(
            width=1.0,
            color=sizeClass['color']))
    return area_values, scatter


def _make_histogram(key, sizeClass, countLabel):
    df = pd.read_hdf(OUT_PATH, key + 'histogram')
    return go.Bar(
        name='%s (%s)' % (sizeClass['name'], countLabel),
        x=100.0 * df['x'],
        y=df['y'],
        marker=go.Marker(color=sizeClass['color']))


def plot_traces(
        plot_type,
        label,
        traces,
        title,
        metadata,
        layout_options,
        suffix=None
):
    suffix = '' if not suffix else ('-' + suffix)

    cd.display.plotly(
        data=traces,
        layout=_get_layout(
            metadata=metadata,
            title=title, **layout_options
        )
    )


def plotComparison(label, name, tracks, metadata):
    metadata = metadata[name]
    expectedDf = pd.read_hdf(OUT_PATH, '{}/expected'.format(name))
    areaValues = np.zeros(len(expectedDf['x']) - 1)

    areaTraces = []
    histTraces = []

    for size_class in cd.shared.SIZE_CLASSES:
        track_count = int(metadata['size_counts'][size_class['id']])

        options = {
            'sizeClass': size_class,
            'key': '{}/{}/'.format(name, size_class['id']),
            'countLabel': locale.format('%d', track_count, grouping=True)
        }

        histTrace = _make_histogram(**options)
        histTraces.append(histTrace)

        areaValues, areaTrace = _make_remainder(
            area_values=areaValues,
            isFirst=cd.shared.SIZE_CLASSES.index(size_class) < 1,
            **options)
        areaTraces.append(areaTrace)

    countLabel = locale.format('%d', metadata['count'], grouping=True)

    areaTraces.append(go.Scatter(
        name='Normal Threshold',
        x=100.0 * expectedDf['x'],
        y=expectedDf['y'],
        mode='lines',
        line=go.Line(
            color='rgba(0, 0, 0, 0.75)',
            dash='dash',
            width=1.0)))

    do_plot_traces = functools.partial(
        plot_traces,
        label=label,
        metadata=metadata)

    do_plot_traces(
        plot_type='HISTOGRAM',
        traces=histTraces,
        title='Distribution of Track {} Deviations ({} Measurements)'.format(
            label, countLabel),
        layout_options={'barmode': 'stack'}
    )

    do_plot_traces(
        plot_type='HIST-LOG',
        suffix='histogram-log',
        traces=histTraces,
        title='Distribution of Track {} Deviations ({} Measurements)'.format(
            label, countLabel),
        layout_options={
            'barmode': 'stack',
            'y_axis': {
                'title': 'Frequency (log)',
                'type': 'log'
            }
        })

    do_plot_traces(
        plot_type='REMAINDER',
        suffix='cdf-remainder',
        traces=areaTraces,
        layout_options={
            'fixed': True,
            'y_axis': {'title': 'Remaining Population (%)'}},
        title=(
            'Inverse Cumulative Distribution of Track ' +
            '{} Deviations ({} Tracks)'
        ).format(label, countLabel)
    )

    do_plot_traces(
        plot_type='REMAINDER-LOG',
        suffix='cdf-remainder-log',
        traces=areaTraces,
        layout_options={
            'fixed': True,
            'y_axis': {
                'title': 'Log Remaining Population (%)',
                'type': 'log'
            }
        },
        title=('Inverse Cumulative Distribution of Track ' +
               '{} Deviations ({} Tracks)').format(label, countLabel))


def run():
    tracks = cd.shared.load_tracks_data()
    with open(METADATA_FILE, 'r') as f:
        metadata = json.loads(f.read())

    do_plot = functools.partial(
        plotComparison,
        tracks=tracks,
        metadata=metadata
    )

    do_plot(name='width', label='Width')
    do_plot(name='length', label='Length')
    do_plot(name='stride', label='Stride Length')
    do_plot(name='pace', label='Pace Length')

run()

