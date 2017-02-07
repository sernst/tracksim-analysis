import functools
import typing

import cauldron as cd
import pandas as pd
from plotly import graph_objs as go

from _measurement_uncertainty import trackways

tracks_df = cd.shared.tracks_df
trackways_df = cd.shared.trackways_df

COLOR_SCALE = [
    [0.0, 'rgba(200, 200, 200, 0.75)'],
    [0.25, 'rgba(0, 0, 0, 0.75)'],
    [1.0, 'rgba(255, 0, 0, 0.75)']
]


def to_position_scatter(tracks: pd.DataFrame) -> typing.List[dict]:
    """

    :param tracks:
    :return:
    """

    def get_data(track: pd.Series) -> dict:
        return dict(
            x=track['x'],
            y=track['y'],
            name=track['name'],
            uid=track['uid'],
            relative_error=track['max_relative']
        )

    return [get_data(track) for _, track in tracks.iterrows()]


def plot_deviations_map(
        trackway_name: str,
        trackway_df: pd.DataFrame,
        marker_size: float = 8,
        progress: float = 0
):
    """

    :param trackway_name:
    :param marker_size:
    :param trackway_df:
    :return:
    """

    track_data = to_position_scatter(trackway_df)

    axis_settings = dict(
        autorange=True,
        showgrid=False,
        zeroline=False,
        showline=False,
        autotick=True,
        ticks='',
        showticklabels=False
    )

    max_relative_error = functools.reduce(
        lambda max_value, track: max(max_value, track['relative_error']),
        track_data,
        0
    )

    sizes = [
        marker_size * (1.0 + 2.0 * t['relative_error'] / max_relative_error)
        for t in track_data
    ]

    entry = trackways_df[trackways_df['trackway'] == trackway_name]

    cd.display.header('{} Relative Error Map'.format(trackway_name))
    cd.display.listing([
        'Width Spread: {}'.format(entry['width_spread'].values[0]),
        'Length Spread: {}'.format(entry['length_spread'].values[0]),
        'Track Count: {}'.format(entry['track_count'].values[0])
    ])

    cd.display.plotly(
        data=go.Scatter(
            x=[t['x'] for t in track_data],
            y=[t['y'] for t in track_data],
            text=[t['name'] for t in track_data],
            mode='markers',
            marker=dict(
                size=sizes,
                color=[100.0 * t['relative_error'] for t in track_data],
                colorscale=COLOR_SCALE,
                showscale=True
            )
        ),
        layout=dict(
            title='Trackway {}'.format(trackway_name),
            hovermode='closest',
            xaxis={**axis_settings},
            yaxis={**axis_settings}
        )
    )


trackways.on(plot_deviations_map, 'BEB-515-2006-1-S-1', tracks_df)
trackways.on(plot_deviations_map, 'BEB-500-2014-1-S-2', tracks_df)
