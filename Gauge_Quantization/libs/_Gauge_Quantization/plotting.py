import typing
import measurement_stats as mstats
import plotly.graph_objs as go
import pandas as pd

from _Gauge_Quantization.windowing.support import Segment


def create_scatter(x, y, error=None, color:str = None, **kwargs) -> dict:
    """

    :param x:
    :param y:
    :param error:
    :param color:
    :return:
    """

    error_y = dict(
        type='data',
        array=error,
        visible=bool(error is not None),
        color=color
    )

    return go.Scatter(
        x=x,
        y=y,
        error_y=error_y,
        mode='markers',
        marker={'color': color},
        **kwargs
    )


def create_line(x, y, color: str = None, **kwargs) -> dict:
    """

    :param x:
    :param y:
    :param color:
    :return:
    """

    return go.Scatter(
        x=x,
        y=y,
        mode='lines',
        line={'color': color},
        **kwargs
    )


def make_ranged_quantity_traces(
        x_start: float,
        x_end: float,
        quantity: mstats.ValueUncertainty,
        color: tuple = (255, 0, 0),
        name: str = None,
        legend_group: str = None,
        show_legend: bool = True
) -> typing.List[dict]:

    value = quantity.value
    upper_value = quantity.value + quantity.uncertainty
    lower_value = quantity.value - quantity.uncertainty

    line_color = 'rgba({},{},{}, 0.5)'.format(*color)
    fill_color = 'rgba({},{},{}, 0.2)'.format(*color)

    value_trace = create_line(
        x=[x_start, x_end],
        y=[value, value],
        color='rgb({},{},{})'.format(*color),
        showlegend=show_legend,
        name=name,
        legendgroup=legend_group
    )

    upper_trace = create_line(
        x=[x_start, x_end],
        y=[upper_value, upper_value],
        color=line_color,
        showlegend=False,
        legendgroup=legend_group,
        fill='tonexty',
        fillcolor=fill_color
    )

    lower_trace = create_line(
        x=[x_start, x_end],
        y=[lower_value, lower_value],
        color=line_color,
        showlegend=False,
        legendgroup=legend_group
    )

    return [lower_trace, upper_trace, value_trace]


def make_segment_traces(
        tracks: pd.DataFrame,
        segment: Segment,
        color: tuple = (255, 0, 0),
        name: str = 'Quantized',
        legend_group: str = 'segments',
        show_legend: bool = None

) -> list:
    start = segment['start_index']
    end = segment['stop_index']

    def get_midpoint_between(before_index: int, after_index: int) -> float:
        positions = tracks['curvePosition'].values

        if before_index < 0:
            return positions[0] - 0.05
        elif after_index >= (len(positions) - 1):
            return positions[-1] + 0.05

        return (positions[before_index] + positions[after_index]) / 2

    should_show_legend = (
        segment['start_index'] == 0
        if show_legend is None
        else show_legend
    )

    return make_ranged_quantity_traces(
        x_start=get_midpoint_between(start - 1, start),
        x_end=get_midpoint_between(end, end + 1),
        quantity=segment.median,
        color=color,
        name=name,
        legend_group=legend_group,
        show_legend=should_show_legend
    )
