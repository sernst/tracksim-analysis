import pandas as pd
import plotly.graph_objs as go
import numpy as np
from _Gauge_Quantization import plotting
from _Gauge_Quantization.windowing import forward as forward_windowing


def compute_unweighted(
        tracks: pd.DataFrame,
        tolerance_fraction: float
) -> dict:
    """ """

    pes_tracks = tracks[tracks['pes'] == 1].copy()  # type: pd.DataFrame
    tolerance = 0.5 * tolerance_fraction * np.median(pes_tracks['width'].values)
    pes_tracks['tolerance'] = tolerance

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

    return dict(
        segments=segments,
        data=[scatter_trace] + segment_traces,
        layout=go.Layout(
            xaxis={'title': 'Trackway Position (m)'},
            yaxis={'title': 'Gauge (m)'}
        )
    )
