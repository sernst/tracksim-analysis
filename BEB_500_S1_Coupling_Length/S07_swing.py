import cauldron as cd
from cauldron import plotting
import measurement_stats as mstats
from plotly import graph_objs as go

FLEXIBILITY_LIMIT = 10

swing = dict()
swing_deviation = dict()


def calculate_swing(df_row, trial):
    """
    :param df_row:
    :param trial:
    :return:
    """

    median = mstats.ValueUncertainty(**trial['couplings']['value'])
    couplings = mstats.values.from_serialized(
        [cl['value'] for cl in trial['couplings']['lengths']]
    )

    max_cl = couplings[0]
    min_cl = couplings[0]
    for cl in couplings[1:]:
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
    swing[trial['id']] = s

    swing_deviation[trial['id']] = s.value / s.uncertainty


df = cd.shared.df
cd.shared.per_trial(df, calculate_swing)
df['swing_deviation'] = [swing_deviation[tid] for tid in df.id]

cd.display.header('Swing', 2)
cd.display.markdown(
    """
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

cd.display.markdown(
    """
    To create a fitness parameter from the swing, the Swing Deviation (SD) is
    calculated as,

    $$$
        @Delta_{swing} = @frac
            { @left| swing - @bar{s} @right| }
            { @delta_{swing} }
    $$$

    where $$@bar{s}$$ is the expectation value against which the deviation is
    being tested. In this case an expectation of zero is used, which represents
    a gait solution without any swing. This has the effect of prioritizing
    solutions that minimize the maximum fluctuation in coupling length. As a
    fitness parameter the deviation of swing does not eliminate trials with
    fluctuations, it only preferences smaller fluctuations over larger ones.
    """
)

cd.display.plotly(
    data=go.Bar(
        y=[swing_deviation[tid] for tid in df.id],
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

