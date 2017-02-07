import cauldron as cd
import pandas as pd
import numpy as np
import measurement_stats as mstats
import plotly.graph_objs as go
from _Gauge_Quantization import plotting

tracks = cd.shared.tracks  # type: pd.DataFrame
trackway_name = cd.shared.TRACKWAY_NAME
pes_tracks = tracks[tracks['pes'] == 1]

layout = go.Layout(
    title='{} Pes Gauge Values Along Trackway'.format(trackway_name),
    xaxis={'title': 'Trackway Position (m)'},
    yaxis={'title': 'Gauge (m)'},
)

scatter_trace = plotting.create_scatter(
    pes_tracks['curvePosition'],
    pes_tracks['simpleGauge'],
    name='Gauges'
)

median_value = np.median(pes_tracks['simpleGauge'].values)
median_absolute_deviation = np.median([
    abs(gauge - median_value)
    for gauge in pes_tracks['simpleGauge']
])
median = mstats.ValueUncertainty(median_value, median_absolute_deviation)

median_traces = plotting.make_ranged_quantity_traces(
    x_start=pes_tracks['curvePosition'].min(),
    x_end=pes_tracks['curvePosition'].max(),
    quantity=median,
    name='Median',
    legend_group='median'
)

cd.display.plotly(
    data=[scatter_trace] + median_traces,
    layout=layout
)

cd.display.markdown(
    """
    We make no assumption that gauge in a trackway is either
    single-valued or have a central tendency. Therefore, we use the median
    and the median absolute deviation as the descriptive statistic instead of
    mean and standard deviation. The results, which are plotted above in red
    are:

     * Median: {{ median }}m
     * MAD: {{ mad }}m
    """,
    median=median.value,
    mad=median.uncertainty
)

cd.shared.unweighted = dict(
    median=median
)
