import typing
import pandas as pd


def get_color(track: pd.Series, tracks: pd.DataFrame, darkest_value: int = 0):
    min_color = min(255, max(0, darkest_value))
    max_uncertainty = max(0.01, tracks['simpleGaugeUnc'].max())
    factor = min(1.0, track['simpleGaugeUnc'] / max_uncertainty)
    color_value = int(round((255 - min_color) * factor)) + min_color
    return 'rgb({color}, {other}, {other})'.format(
        color=color_value,
        other=int(round((1 - factor) * min_color))
    )


def create_attribute(name: str, value) -> str:
    return '{}="{}"'.format(name, value)


def create_tag(name: str, attributes: dict) -> str:
    attrs = [create_attribute(n, v) for n, v in attributes.items()]
    return '<{} {}></{}>'.format(name, ' '.join(attrs), name)


def create_transform(tracks: pd.DataFrame) -> dict:
    out = dict(
        x_min=tracks['x'].min(),
        x_max=tracks['x'].max(),
        y_min=tracks['y'].min(),
        y_max=tracks['y'].max()
    )

    delta_x = out['x_max'] - out['x_min']
    delta_y = out['y_max'] - out['y_min']

    scale = min(
        1920 / max(1, delta_x),
        800 / max(1, delta_y)
    )

    padding = 40

    view_box = [
        -padding,
        -padding,
        int(round(scale * delta_x + 2 * padding)),
        int(round(scale * delta_y + 2 * padding))
    ]

    out.update(
        scale=scale,
        delta_x=delta_x,
        delta_y=delta_y,
        view_box=view_box,
        padding=40
    )

    return out


def transform_x(position: float, transformation: dict) -> float:
    x_min = transformation['x_min']
    scale = transformation['scale']

    return round(scale * (position - x_min))


def transform_y(position: float, transformation: dict) -> float:
    y_min = transformation['y_min']
    scale = transformation['scale']

    return round(scale * (-position - y_min))


def make_circles(tracks: pd.DataFrame, transformation: dict) -> list:
    def make_circle(track: pd.Series):
        return create_tag('circle', {
            'r': 16,
            'cx': transform_x(track['x'], transformation),
            'cy': transform_y(track['y'], transformation),
            'style': 'fill:{}'.format(get_color(track, tracks))
        })

    return [make_circle(row) for index, row in tracks.iterrows()]


def make_lines(tracks: pd.DataFrame, transformation: dict) -> list:
    def make_line(start: pd.Series, end: pd.Series) -> str:
        return create_tag('line', {
            'stroke': 'rgba(0, 0, 0, 0.2)',
            'stroke-width': '2',
            'stroke-dasharray': '5,5',
            'x1': transform_x(start['x'], transformation),
            'y1': transform_y(start['y'], transformation),
            'x2': transform_x(end['x'], transformation),
            'y2': transform_y(end['y'], transformation)
        })

    previous = pd.Series(dict(
        x=transformation['x_min'],
        y=tracks.iloc[0]['y']
    ))
    lines = []

    for index, row in tracks.iterrows():
        lines.append(make_line(previous, row))
        previous = row

    if previous['x'] < transformation['x_max']:
        lines.append(make_line(previous, pd.Series(dict(
            x=transformation['x_max'],
            y=previous['y']
        ))))

    return lines


def make_gauge_lines(tracks: pd.DataFrame, transformation: dict) -> list:
    def make_line(track: pd.Series) -> str:
        delta = track['simpleGauge'] * (-1 if track['left'] else 1)
        y_gauge = track['y'] + delta

        line = create_tag('line', {
            'stroke': get_color(track, tracks, 150),
            'stroke-width': '4',
            'x1': transform_x(track['x'], transformation),
            'y1': transform_y(track['y'], transformation),
            'x2': transform_x(track['x'], transformation),
            'y2': transform_y(y_gauge, transformation)
        })

        circle = create_tag('circle', {
            'r': 6,
            'style': 'fill: {}'.format(get_color(track, tracks, 150)),
            'cx': transform_x(track['x'], transformation),
            'cy': transform_y(y_gauge, transformation)
        })

        return ''.join([line, circle])

    return [make_line(t) for i, t in tracks.iterrows()]


def draw_tracks(tracks: pd.DataFrame) -> str:
    transformation = create_transform(tracks)
    children = (
        make_lines(tracks[tracks['left'] == True], transformation) +
        make_lines(tracks[tracks['left'] == False], transformation) +
        make_gauge_lines(tracks, transformation) +
        make_circles(tracks, transformation)
    )

    return '<svg xmlns="{}" xmlns:xlink="{}" viewbox="{}">{}</svg>'.format(
        'http://www.w3.org/2000/svg',
        'http://www.w3.org/1999/xlink',
        ' '.join(['{}'.format(value) for value in transformation['view_box']]),
        ''.join(children)
    )
