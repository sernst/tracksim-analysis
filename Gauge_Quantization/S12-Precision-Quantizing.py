import cauldron as cd
import pandas as pd
import plotly.graph_objs as go
from _Gauge_Quantization import precision_windowing
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

cd.display.plotly(
    data=[scatter_trace] + segment_traces,
    layout=layout
)
