import cauldron as cd
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from _Gauge_Quantization.windowing import forward as forward_windowing
from _Gauge_Quantization import plotting

tracks = cd.shared.tracks  # type: pd.DataFrame
trackway_name = cd.shared.TRACKWAY_NAME


def make_segments(fraction: float) -> list:
    """ """

    pes_tracks = tracks[tracks['pes'] == 1].copy()  # type: pd.DataFrame
    tolerance = 0.5 * fraction * np.median(pes_tracks['width'].values)
    pes_tracks['tolerance'] = tolerance

    layout = go.Layout(
        title='{} Quantized Pes Gauges (Tolerance: {}cm)'.format(
            trackway_name,
            round(2 * 100 * tolerance)
        ),
        xaxis={'title': 'Trackway Position (m)'},
        yaxis={'title': 'Gauge (m)'}
    )

    scatter_trace = plotting.create_scatter(
        pes_tracks['curvePosition'],
        pes_tracks['simpleGauge'],
        color='rgba(200, 200, 200, 1)',
        name='Gauges'
    )

    segments = forward_windowing.compute(
        pes_tracks['simpleGauge'].tolist(),
        pes_tracks['tolerance'].tolist(),
        weighted=False
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

    return segments


make_segments(0.25)
make_segments(0.5)
make_segments(1.0)
