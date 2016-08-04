import math

import cauldron as cd
from cauldron import plotting
import measurement_stats as mstats
from plotly import graph_objs as go

swing = dict()

WINDOW_SIZE = 2


def average_coupling_lengths(df_row, trial):
    """
    Calculate the average coupling lengths at each data sample in the trial
    using globally specified WINDOW_SIZE.

    :param df_row:
    :param trial:
    :return:
        A list of averaged coupling lengths for the specified trial
    """

    couplings = mstats.values.from_serialized(
        [cl['value'] for cl in trial['couplings']['lengths']]
    )
    weighted = []
    unweighted = []

    for index in range(len(couplings)):
        segment = couplings[index:index + WINDOW_SIZE]
        if len(segment) < WINDOW_SIZE:
            break

        wxs = 0.0
        ws = 0.0
        for v in segment:
            w = 1.0 / (v.raw_uncertainty ** 2)
            wxs += w * v.raw
            ws += w

        weighted.append(mstats.ValueUncertainty(
            wxs / ws,
            1.0 / math.sqrt(ws)
        ))

        # weighted.append(mstats.mean.weighted(segment))
        unweighted.append(sum(segment) / len(segment))

    return weighted, unweighted


def calculate_swing(df_row, trial):
    """
    :param df_row:
    :param trial:
    :return:
    """

    median = mstats.ValueUncertainty(**trial['couplings']['value'])
    weighted, unweighted = average_coupling_lengths(df_row, trial)

    max_cl = weighted[0]
    min_cl = weighted[0]
    for cl in weighted[1:]:
        max_cl = mstats.value.maximum(max_cl, cl)
        min_cl = mstats.value.minimum(min_cl, cl)

    s = abs(max_cl - min_cl) / median.value
    s.freeze()
    swing[trial['id']] = s


df = cd.shared.df
cd.shared.per_trial(df, calculate_swing)

cd.display.markdown(
    """
    Swing
    -----

    Again consider a fictional trackway where two simulation trials (a and b)
    produce the following two coupling length plots:

    ![Swing Example 1](assets/Swing-Example-1.svg)

    Each trial has two persistent deviation regions, one large and one small.
    The only difference is that the smaller persistent deviation regions are
    positive in trial _a_ and negative in trial _b_. Calculating the _PRSS_
    value for these two trials yields the same value, $$ PRSS = 0.025 $$. The
    _PRSS_ parameter doesn't account for differences in the sign of the
    residuals, which characterizes a greater range of coupling length values
    for trial _b_ than trial _a_. Another parameter is needed to express the
    global range of coupling length values within a trial.

    We define the parameter, which we will call _swing_, as the difference
    between minimum and maximum coupling length values:

    $$$
        swing = @frac{ @left|CL_{max} - CL_{min} @right|}{CL_{median}}
    $$$

    It is normalized by the median coupling length value to remove the same
    scaling issue that arose in the _PRSS_ formulation when comparing trials
    with different median coupling lengths. The calculated _swing_ for the
    two example trials are $$ swing_a = 0.15 $$ and $$ swing_b = 0.2 $$. The
    smaller _swing_ for trial _a_ suggests that it is a _better_ solution
    for the given trackway than trial _b_. The trackmaker could have traversed
    the trackway under the conditions in trial _a_ with less alteration of its
    posture.

    But the _swing_ formulation is not yet complete. We previously established
    the  importance of persistence in the formulation of the _PRSS_ parameter
    and it pertains to _swing_ as well. A single-sampled deviation can be
    attributed noise, while multi-sampled ones indicate changes in the posture
    of the trackmaker. To illustrate this, consider a second fictional trackway
    where two simulation trials (a and b) produce the following two coupling
    length plots:

    ![Swing Example 2](assets/Swing-Example-2.svg)

    The only difference between trial _a_ and trial _b_ in this example is the
    third coupling length sample. In trial _a_ the third sample has a zero
    deviation from the baseline value, while in trial _b_ the third sample has
    a non-zero deviation from the baseline value. Using the formulation for
    _swing_ outlined above, these two example trials have the same swing value
    despite the greater persistence of a deviation in trial _b_ than in trial
    _a_. An efficient way to resolve this issue is to introduce a forward
    moving average, which is generally defined in the form:

    $$$
        @overline{x}_i = @frac{x_i + x_{i+1}}{2}
    $$$

    Here the average value of a sample $$ @overline{x_{i}} $$ is the mean
    of the original sample $$ x_i $$ and its next nearest neighbor. This
    mean is unweighted with respect to the uncertainties of the samples, which
    is not suitable for coupling lengths. Instead a weighted version of the
    forward moving average is used,


    $$$
        @overline{CL}_i = @frac
            {
                @tfrac{CL_i}{@sigma_i^2} +
                @tfrac{CL_{i+1}}{@sigma_{i+1}^2}
            }
            { @sigma_i + @sigma_{i+1} }
    $$$

    Where $$ @sigma_i $$ and $$ @sigma_{i+1} $$ are the uncertainties in the
    $$i$$ and $$i+1$$ coupling length values.

    The weighted averaged coupling length values can then be substituted into
    the previous swing equation as,

    $$$
        swing = @frac
        {
            @left|@overline{CL}_{max} -
            @overline{CL}_{min} @right|
        }
        { CL_{median} }
    $$$

    This updated _swing_ formulation now properly distinguishes between the
    two trials from the previous example with a higher _swing_ value for trial
    _b_ than for trial _a_. Applying this _swing_ formulation to BEB 500 S1
    yields:
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
        y_label='Swing'
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
    In the same fashion as the _PRSS_ parameter, the _swing_ parameter needs
    to be converted into fitness parameter for comparison of a all trials
    among their peers. The approach used for _PRSS_ is used for _swing_.
    The lowest swing value among the trials is used as the highest fitness
    value, and all other trials are compared to it using the deviation
    significance calculation,

    $$$
        @Delta_{swing} = @frac
            { @left| swing_i - swing_{min} @right| }
            { @sqrt{ @sigma_i^2 + @sigma_{min}^2 } }
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

