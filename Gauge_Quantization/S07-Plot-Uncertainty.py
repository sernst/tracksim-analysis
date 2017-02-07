import math

import cauldron as cd
import measurement_stats as mstats
import pandas as pd
import plotly.graph_objs as go

from _Gauge_Quantization import plotting

tracks = cd.shared.tracks  # type: pd.DataFrame
trackway_name = cd.shared.TRACKWAY_NAME
unweighted = cd.shared.unweighted
pes_tracks = tracks[tracks['pes'] == 1]

layout = go.Layout(
    title='{} Pes Gauge Values Along Trackway'.format(trackway_name),
    xaxis={'title': 'Trackway Position (m)'},
    yaxis={'title': 'Gauge (m)'}
)

dist = mstats.create_distribution(
    pes_tracks['simpleGauge'].tolist(),
    pes_tracks['simpleGaugeUnc'].tolist()
)
pop = mstats.distributions.population(dist)
median_value = mstats.distributions.percentile(pop)
mad = mstats.distributions.weighted_median_average_deviation(pop)
median = mstats.ValueUncertainty(median_value, mad)

scatter_trace = plotting.create_scatter(
    pes_tracks['curvePosition'],
    pes_tracks['simpleGauge'],
    pes_tracks['simpleGaugeUnc'],
    name='Gauges'
)

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
    Once again we make no assumption that gauge in a trackway is either
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

median_compare = unweighted['median']  # type: mstats.ValueUncertainty

deviation = (
    abs(median.value - median_compare.value) /
    math.sqrt(median.uncertainty ** 2 + median_compare.uncertainty ** 2)
)

cd.display.markdown(
    """
    With a deviation of {{ deviation }}%, there isn't a significant disagreement
    between the median values of the uncertainty-weighted and unweighted median
    values. However, this isn't surprising given that a global median is a
    highly reductive statistic for a potentially variable value. For the global
    median to be significantly different, there would need to be some amount
    of preservation bias on either the lower or upper tail of the distribution.

    But when it comes to a gauge analysis, what we're really interested in are
    deviations, not a single global value. This is where the unweighted and
    weighted analyses begin to differ significantly.
    """,
    deviation=int(100 * deviation)
)

cd.shared.weighted = dict(
    median=median
)
