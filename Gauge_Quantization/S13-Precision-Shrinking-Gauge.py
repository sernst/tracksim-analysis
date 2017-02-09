import cauldron as cd
import plotly.graph_objs as go

from _Gauge_Quantization import generator
from _Gauge_Quantization import plotting
from _Gauge_Quantization.windowing import forward as forward_windowing
from _Gauge_Quantization.windowing import precision as precision_windowing
from _Gauge_Quantization.generator import draw

tracks = generator.create(
    12,
    (1, 0.3, 0.3),
    (2, 0.3, 0.01),
    (4, 0.3, 0.05),
    (8, 0.1, 0.02)
)
tracks['width'] = 0.3

cd.display.markdown(
    """
    ## Precision Windowing the Shrinking Gauge

    To get a better understanding of the benefit of precision-windowed
    clustering we return to the idealized shrinking gauge trackway we
    investigated earlier with one change. This time we assign a variable
    uncertainty values to the positions of all tracks in the trackway with
    the very first track having a much larger uncertainty than the rest of
    the trackway. The uncertainty distribution of the resulting gauges then
    looks like:
    """
)

cd.display.plotly(
    data=go.Bar(
        x=tracks['curvePosition'],
        y=tracks['simpleGaugeUnc']
    ),
    layout=dict(
        title='Gauge Uncertainties',
        xaxis={'title': 'Track Position (m)'},
        yaxis={'title': 'Gauge Uncertainty (m)'}
    )
)

cd.display.markdown(
    """
    Because gauge calculations depend on the nearest opposing limb's tracks,
    this results in lower precision gauge values for the first two tracks in
    the trackway and then a uniform, higher precision throughout the remainder
    of the trackway.

    The track diagram now looks like:
    """
)

cd.display.svg(draw.draw_tracks(tracks))

cd.display.markdown(
    """
    where the redness of a track is an indication of the amount of uncertainty
    within the trackway.

    We can now run the uncertainty-based clustering on this idealized trackway
    using both the forward and precision algorithms and compare:
    """
)

layout = go.Layout(
    title='Forward-Window Gauge Clustering',
    xaxis={'title': 'Trackway Position (m)'},
    yaxis={'title': 'Gauge (m)'}
)

scatter_trace = plotting.create_scatter(
    tracks['curvePosition'],
    tracks['simpleGauge'],
    tracks['simpleGaugeUnc'],
    color='rgba(200, 200, 200, 1)',
    name='Gauges'
)

forward_segments = forward_windowing.compute(
    tracks['simpleGauge'].tolist(),
    tracks['simpleGaugeUnc'].tolist()
)

cd.display.plotly(
    data=[scatter_trace] + [
        trace
        for s in forward_segments
        for trace in plotting.make_segment_traces(tracks, s)
    ],
    layout=layout
)

layout = go.Layout(
    title='Precision-Window Gauge Clustering',
    xaxis={'title': 'Trackway Position (m)'},
    yaxis={'title': 'Gauge (m)'}
)

scatter_trace = plotting.create_scatter(
    tracks['curvePosition'],
    tracks['simpleGauge'],
    tracks['simpleGaugeUnc'],
    color='rgba(200, 200, 200, 1)',
    name='Gauges'
)

precision_segments = precision_windowing.compute(
    tracks['simpleGauge'].tolist(),
    tracks['simpleGaugeUnc'].tolist()
)

cd.display.plotly(
    data=[scatter_trace] + [
        trace
        for s in precision_segments
        for trace in plotting.make_segment_traces(tracks, s)
    ],
    layout=layout
)

forward_cumulative_variance = sum([
    s.median.uncertainty * len(s.quantities)
    for s in forward_segments
])

precision_cumulative_variance = sum([
    s.median.uncertainty * len(s.quantities)
    for s in precision_segments
])

improvement = (
    (forward_cumulative_variance - precision_cumulative_variance) /
    precision_cumulative_variance
)

cd.display.markdown(
    """
    The segmented results of the two clustering approaches are different. The
    first segment in the forward-windowed result has a much higher dispersion
    than the precision-windowed result because the forward-windowed result
    began its first segment with the lowest precision gauge value in the
    trackway. This causes a larger accumulated dispersion for the entire
    segment as well as the accumulated total dispersion over the trackway.

    To better quantify this difference, we can sum the deviations over the
    entire trackway, which yields {{ forward_total }}m for the forward-windowed
    result versus {{ precision_total }}m for the precision-windowed result.
    Precision clustering has both removed the arbitrary direction biasing and
    provided a {{ ratio }}% reduction in total segment dispersion.
    """,
    forward_total=forward_cumulative_variance,
    precision_total=precision_cumulative_variance,
    ratio=int(round(100 * improvement))
)
