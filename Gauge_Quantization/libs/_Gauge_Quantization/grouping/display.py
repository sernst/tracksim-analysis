import typing
import pandas as pd
from _Gauge_Quantization.grouping import SegmentGroup
from _Gauge_Quantization.windowing import support

COLORS = (
    (31, 119, 180),
    (255, 127, 14),
    (44, 160, 44),
    (214, 39, 40),
    (148, 103, 189),
    (140, 86, 75),
    (227, 119, 194),
    (127, 127, 127),
    (188, 189, 34),
    (23, 190, 207)
)


def create_style(name: str, value) -> str:
    return '{}:{}'.format(name, value)


def create_attribute(name: str, value) -> str:
    if isinstance(value, dict):
        values = [create_style(n, v) for n, v in value.items()]
        attr_value = ';'.join(values)
    else:
        attr_value = value

    return '{}="{}"'.format(name, attr_value)


def create_tag(
        name: str, attributes: dict,
        body: typing.Union[str, list]
) -> str:
    attrs = [create_attribute(n, v) for n, v in attributes.items()]
    return '<{name} {attrs}>{body}</{name}>'.format(
        name=name,
        attrs=' '.join(attrs),
        body=''.join(body) if hasattr(body, 'index') else '{}'.format(body)
    )


def get_length(segment: support.Segment, tracks: pd.DataFrame) -> float:
    bounds = support.get_segment_bounds(segment.quantities, tracks)
    return abs(bounds[1] - bounds[0])


def to_dom(group: SegmentGroup, tracks: pd.DataFrame) -> str:
    """

    :param group:
    :param tracks:
    :return:
    """

    group_length = sum([get_length(s, tracks) for s in group.segments])
    total_length = tracks['curvePosition'].max()

    length_percent = int(round(100 * group_length / total_length))
    group_length = 0.01 * round(100 * group_length)

    styles = {
        'padding': '1em',
        'color': 'rgb({},{},{})'.format(*COLORS[group.index % len(COLORS)])
    }

    title_styles = {
        'font-size': '1.4em'
    }

    return create_tag('div', {'style': styles}, [
        create_tag(
            'div',
            {'style': title_styles},
            'Group {}'.format(group.index + 1)
        ),
        create_tag('div', { 'style': {'padding': '0.5em 1em'}}, [
            create_tag('div', {}, 'Gauge: {}m'.format(group.median.html_label)),
            create_tag('div', {}, 'Width Normalized: {}'.format(
                group.normalized_median.html_label
            )),
            create_tag('div', {}, 'Total Length: {}m'.format(group_length)),
            create_tag('div', {}, 'Length of Trackway: {}%'.format(
                length_percent
            ))
        ])
    ])
