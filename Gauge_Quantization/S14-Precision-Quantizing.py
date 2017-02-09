import cauldron as cd
import pandas as pd
import plotly.graph_objs as go
from _Gauge_Quantization.windowing import precision as precision_windowing
from _Gauge_Quantization import plotting

tracks = cd.shared.tracks  # type: pd.DataFrame
trackway_name = cd.shared.TRACKWAY_NAME
pes_tracks = tracks[tracks['pes'] == 1]

layout = go.Layout(
    title='{} Pes Gauge Values Along Trackway'.format(trackway_name),
    xaxis={'title': 'Trackway Position (m)'},
    yaxis={'title': 'Gauge (m)'}
)

scatter_trace = plotting.create_scatter(
    pes_tracks['curvePosition'],
    pes_tracks['simpleGauge'],
    pes_tracks['simpleGaugeUnc'],
    color='rgba(200, 200, 200, 1)',
    name='Gauges'
)


segments = precision_windowing.compute(
    pes_tracks['simpleGauge'].tolist(),
    pes_tracks['simpleGaugeUnc'].tolist()
)
segment_traces = [
    trace
    for s in segments
    for trace in plotting.make_segment_traces(pes_tracks, s)
]

cd.display.markdown(
    """
    ## Precision Windowing {{ trackway_name }}

    Applying the precision-windowed clustering algorithm to the
    {{ trackway_name }} trackway yields a segmentation of:
    """,
    trackway_name=trackway_name
)

cd.display.plotly(
    data=[scatter_trace] + segment_traces,
    layout=layout
)

cd.display.markdown(
    """
    which is also noticeably different than the forward-windowed result
    previously shown. We now have a highly robust and objective way of
    segmenting gauge values within real trackways, which allows
    us to rigorously present results on the variations of gauges within
    trackways.
    """
)

cd.shared.segments = segments
