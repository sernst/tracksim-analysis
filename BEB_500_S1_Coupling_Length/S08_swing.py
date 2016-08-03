import math

import cauldron as cd
from cauldron import plotting
import measurement_stats as mstats
from plotly import graph_objs as go

swing = dict()
residuals = dict()

WINDOW_SIZE = 2


def calculate_residuals(df_row, trial):
    """
    :param df_row:
    :param trial:
    :return:
    """

    median = mstats.ValueUncertainty(**trial['couplings']['value'])
    couplings = mstats.values.from_serialized(
        [cl['value'] for cl in trial['couplings']['lengths']]
    )
    out = []

    for index in range(len(couplings)):
        segment = couplings[index:index + WINDOW_SIZE]
        if len(segment) < WINDOW_SIZE:
            break
        out.append(sum(segment) / len(segment))

    residuals[trial['id']] = out


def calculate_swing(df_row, trial):
    """
    :param df_row:
    :param trial:
    :return:
    """

    median = mstats.ValueUncertainty(**trial['couplings']['value'])
    prss = residuals[trial['id']]

    max_cl = prss[0]
    min_cl = prss[0]
    for cl in prss[1:]:
        max_threshold = max_cl.value - 2 * max_cl.uncertainty
        threshold = cl.value - 2 * cl.uncertainty

        if threshold > max_threshold:
            max_cl = cl
        elif threshold == max_threshold and cl.value > max_cl.value:
            max_cl = cl

        min_threshold = min_cl.value + 2 * min_cl.uncertainty
        threshold = cl.value + 2 * cl.uncertainty

        if threshold < min_threshold:
            min_cl = cl
        elif threshold == min_threshold and cl.value < min_cl.value:
            min_cl = cl

    s = 100 * abs(max_cl - min_cl) / median.value
    s.freeze()
    swing[trial['id']] = s


df = cd.shared.df
cd.shared.per_trial(df, calculate_residuals)
cd.shared.per_trial(df, calculate_swing)

cd.display.markdown(
    """
    Swing
    -----

    __TEXT NOT UPDATED YET__

    The RMSD fitness parameter developed above considers the accumulation of
    deviations from the median coupling length over the course of the
    simulation. This could be due to small but consistent deviations, a
    few large ones or a combination of the two. A complimentary fitness
    parameter with RMSD would be one that isolates the extremes and ignores
    the the smaller accumulations.

    Calculating the swing, the difference between minimum and maximum sample
    values, gives us an indication of the magnitude of fluctuation in a
    particular trial,

    $$$
        swing = @frac{ @left|CL_{max} - CL_{min} @right|}{CL_{median}}
    $$$

    The swing has been normalized by the median coupling length for comparison
    between trials.
    """
)
cd.display.plotly(
    data=cd.shared.create_scatter(
        df,
        [swing[tid].value for tid in df.id],
        [swing[tid].uncertainty for tid in df.id]
    ),
    layout=plotting.create_layout(
        title='Normalized Swing by Trial',
        x_label='Trial Index (#)',
        y_label='Swing (%)'
    )
)

swing_comparisons = dict()
minimum_swing = mstats.values.minimum(swing.values())

for key, res in swing.items():
    swing_comparisons[key] = abs(
        (res.value - minimum_swing.value) /
        math.sqrt(res.uncertainty ** 2 + minimum_swing.uncertainty ** 2)
    )

cd.display.markdown(
    """
    In the same fashion as the normalized RSS parameter above, a parameter of
    fitness has to be created from the swing values that allows for the global
    comparison of a trial relative to all of its peers. The same method is used
    for swing as well. The lowest swing value among the trials is used as the
    highest fitness value, and all other trials are compared to it using a
    deviation significance calculation,

    $$$
        @Delta_{swing} = @frac
            { @left| swing_i - swing_{min} @right| }
            { @sqrt{ @delta_i^2 + @delta_{min}^2 } }
    $$$
    """
)

df['swing'] = [swing_comparisons[tid] for tid in df.id]

cd.display.plotly(
    data=go.Bar(
        y=df.swing,
        text=df.short_id,
        marker=dict(
            color=df.color
        )
    ),
    layout=plotting.create_layout(
        title='Swing Deviation',
        x_label='Trial Index (#)',
        y_label='Fractional Deviation'
    )
)

