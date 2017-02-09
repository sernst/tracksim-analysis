import cauldron as cd
import plotly.graph_objs as go

from _Gauge_Quantization import grouping
from _Gauge_Quantization.grouping import display
from _Gauge_Quantization import plotting

segments = cd.shared.segments
tracks = cd.shared.tracks
pes_tracks = tracks[tracks['pes'] == 1]
trackway_name = cd.shared.TRACKWAY_NAME


cd.display.markdown(
    """
    ## {{ trackway_name }} Segment Grouping

    Applying the group clustering algorithm to the precision-windowed
    segmentation of the {{ trackway_name }} trackway, we arrive at the
    following plot where each group of segments is assigned a different
    color:
    """,
    trackway_name=trackway_name
)

layout = go.Layout(
    title='{} Grouped Gauge Values'.format(trackway_name),
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


def get_segment_traces(group, segment):
    color = display.COLORS[group.index % len(display.COLORS)]
    return plotting.make_segment_traces(
        pes_tracks,
        segment,
        color=color,
        name='Gauge #{}'.format(group.index + 1),
        show_legend=(group.segments.index(segment) < 1),
        legend_group='gauge-group-{}'.format(group.index)
    )

groups = grouping.combine(segments, pes_tracks)
group_traces = [
    trace
    for group in groups
    for segment in group.segments
    for trace in get_segment_traces(group, segment)
]

cd.display.plotly(
    data=[scatter_trace] + group_traces,
    layout=layout
)

cd.display.markdown(
    """
    A rigorous analysis of the gauge values in this trackway yields distinct
    gauge values of:
    """
)

cd.display.html(''.join([display.to_dom(g, pes_tracks) for g in groups]))
