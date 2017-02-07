import cauldron as cd
import math
import measurement_stats as mstats
import plotly.graph_objs as go
import numpy as np


def calculate_distance(
        pre: dict,
        post: dict,
        x: mstats.ValueUncertainty,
        y: mstats.ValueUncertainty
) -> mstats.ValueUncertainty:
    delta_y = post['y'] - pre['y']
    delta_x = post['x'] - pre['x']

    numerator_1 = delta_y * x
    numerator_2 = delta_x * y
    numerator_3 = post['x'] * pre['y']
    numerator_4 = post['y'] * pre['x']
    numerator = abs(numerator_1 - numerator_2 + numerator_3 - numerator_4)

    denominator = math.sqrt(delta_x ** 2 + delta_y ** 2)
    if denominator == 0:
        return mstats.ValueUncertainty(0, 1)

    result = numerator / denominator  # type: mstats.ValueUncertainty
    return result

pre_track = dict(
    x=mstats.ValueUncertainty(1, 0.01),
    y=mstats.ValueUncertainty(1, 0.01)
)

post_track = dict(
    x=mstats.ValueUncertainty(2, 0.05),
    y=mstats.ValueUncertainty(2, 0.05)
)

x_quantities = mstats.values.join(
    list(np.linspace(
        pre_track['x'].value - 0.25,
        post_track['x'].value + 0.25,
        20
    )),
    0.01
)
y_quantities = mstats.values.join(
    list(np.linspace(
        pre_track['y'].value - 0.25,
        post_track['y'].value + 0.25,
        20
    )),
    0.01
)

distances = []

for y_quantity in y_quantities:
    distances.append([
        calculate_distance(pre_track, post_track, x_quantity, y_quantity)
        for x_quantity in x_quantities
    ])

distance_uncertainties = []
for distance_row in distances:
    distance_uncertainties.append([d.uncertainty for d in distance_row])

contour_trace = go.Contour(
    z=distance_uncertainties,
    x=[x.value for x in x_quantities],
    y=[y.value for y in y_quantities],
    colorscale='Blues'
)

scatter_trace = go.Scatter(
    x=[pre_track['x'].value, post_track['x'].value],
    y=[pre_track['y'].value, post_track['y'].value],
    mode='lines+markers',
    marker={'color': 'black', 'size': 12},
    line={'color': 'white', 'width': 2}
)

cd.display.markdown(
    """
    # Visualizing Uncertainties

    Consider a case where the opposing limb has tracks located at positions
    ({{ pre_x }}m, {{ pre_y}}m) and ({{ post_x }}m, {{ post_y }}m). We have
    assigned a larger uncertainty to the second of these tracks than the first
    to emphasize the impact the uncertainties of each track have on the result.

    Then we sample multiple positions in the spatial region around these
    tracks with a sample track that has an uncertainty of &#177; 0.01m.
    The collected uncertainties at each of these sampled positions can then be
    used to generate a contour plot of the spatial dependence of the
    uncertainty calculations for a sample track as shown in the following plot.
    """,
    pre_x=pre_track['x'].html_label,
    pre_y=pre_track['y'].html_label,
    post_x=post_track['x'].html_label,
    post_y=post_track['y'].html_label,
)

cd.display.plotly(
    data=[contour_trace, scatter_trace],
    layout=dict(
        title='Example Spatial Distribution of Gauge Uncertainties',
        xaxis={'title': 'Position (m)'},
        yaxis={'title': 'Position (m)'},
    )
)

cd.display.markdown(
    """
    What we can see from the plot is that the uncertainties in the gauge values
    are always larger than the uncertainties of the tracks used to calculate
    them. While there is a greater dependence on the uncertainty of the closer
    opposing limb's track, the uncertainty of all three tracks contribute to
    the uncertainty in the gauge at all positions.

    With a better understanding of how uncertainty has been calculated for
    a particular gauge from the uncertainties in the positions of the tracks
    used to calculate the value, we can now apply these uncertainty formulas
    to the gauge values for the {{ TRACKWAY_NAME }} trackway and see the
    results.
    """
)