import functools

import cauldron as cd
from cauldron import plotting
import measurement_stats as mstats
import plotly.graph_objs as go
import numpy as np

df = cd.shared.df

SCALING = 0.12
SEGMENT_MIN = 1.23
SEGMENT_MAX = 2.1

cd.display.markdown(
    """
    The stem plot of fitness is useful for placing individual trials
    within the context of the their peers, but it hides one critical piece of
    information: the uncertainty in the coupling length for each trial.

    To include uncertainty each fitness value needs to be represented as a
    Gaussian kernel function with a width based on the uncertainty in coupling
    length for that trial. Each Gaussian is weighted according to it fitness
    such that a low fitness value produces a correspondingly smaller Gaussian.

    The sum over all Gaussian kernels leads to a fitness distribution by
    coupling length.
    """
)

measurements = mstats.values.join(
    df['coupling_length'].tolist(),
    df['uncertainty'].tolist()
)

distribution = mstats.create_distribution(measurements)
x_values = mstats.distributions.adaptive_range(distribution, 4)
y_values = distribution.heighted_probabilities_at(x_values, df['fitness'])

distribution_trace = go.Scatter(
    x=x_values,
    y=y_values,
    name='Distribution',
    mode='lines',
    fill='tozeroy'
)

cd.display.plotly(
    distribution_trace,
    layout=plotting.create_layout(
        title='Kernel Density Solution Fitness',
        x_label='Coupling Length (m)',
        y_label='Fitness Density (AU)'
    )
)

max_value = functools.reduce(
    lambda a, b: (a if a[1] > b[1] else b),
    zip(x_values, y_values),
    (0, 0)
)


def to_numeric_label(value):
    return '{:0.1f}'.format(mstats.value.round_to_order(value, -1))


cd.display.markdown(
    """
    This distribution allows us to find the point of maximum fitness and
    its corresponding coupling length. In this case it turns out to be a
    coupling length of {{ coupling_length }} meters with a fitness density
    value of {{ fitness }}.

    This single coupling length value does not account for the spread of high
    fitness values around it. To get a better estimate of the coupling length,
    we focus on the interval in the distribution in which the highest peak
    resides, and fit that region to a Gaussian:
    """,
    coupling_length=to_numeric_label(max_value[0]),
    fitness=to_numeric_label(max_value[1])
)

points = [
    p for p in zip(x_values, y_values)
    if SEGMENT_MIN < p[0] < SEGMENT_MAX
    ]
x_segment_values, y_segment_values = zip(*points)

segment_trace = go.Scatter(
    x=x_segment_values,
    y=y_segment_values,
    mode='lines',
    name='Region',
    line=go.Line(
        color=plotting.get_color(1, 1.0),
        width=4
    )
)

population = mstats.distributions.population(distribution, 4096)
population = [x for x in population if SEGMENT_MIN < x < SEGMENT_MAX]

coupling_length = mstats.ValueUncertainty(
    np.median(population),
    mstats.distributions.weighted_median_average_deviation(population)
)

gaussian_fit = mstats.create_distribution([coupling_length])

y_gauss_values = gaussian_fit.probabilities_at(x_values)
y_gauss_values = [SCALING * y for y in y_gauss_values]

gaussian_trace = go.Scatter(
    x=x_values,
    y=y_gauss_values,
    mode='lines',
    name='Region Fit',
    line=go.Line(
        color='rgba(0, 0, 0, 0.75)',
        dash='dash',
        width=3
    )
)

cd.display.plotly(
    [distribution_trace, segment_trace, gaussian_trace],
    layout=plotting.create_layout(
        title='Kernel Density Solution Fitness',
        x_label='Coupling Length (m)',
        y_label='Fitness Density (AU)'
    )
)


cd.display.markdown(
    """
    The resulting best estimate of the coupling length is then: {{ cl }} m
    """,
    cl=coupling_length.html_label
)


