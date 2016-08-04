import math

import cauldron as cd
from cauldron import plotting
import measurement_stats as mstats
import plotly.graph_objs as go

unnormalized = dict()
persistence = dict()
df = cd.shared.df


def calculate_persistence(df_row, trial):
    """
    Calculates the persistence residual values for each trial

    :param df_row:
    :param trial:
    :return:
    """

    median = mstats.ValueUncertainty(**trial['couplings']['value'])
    couplings = mstats.values.from_serialized(
        [cl['value'] for cl in trial['couplings']['lengths']]
    )

    # Unnormalized
    residuals = [abs(cl - median.value) for cl in couplings]

    prss = mstats.ValueUncertainty(0, 0.0000001)
    for index, residual in enumerate(residuals[:-1]):
        prss += residual * residuals[index + 1]

    prss.freeze()
    unnormalized[trial['id']] = prss

    # Normalized
    residuals = [abs(cl / median.value - 1) for cl in couplings]

    prss = mstats.ValueUncertainty(0, 0.0000001)
    for index, residual in enumerate(residuals[:-1]):
        prss += residual * residuals[index + 1]

    prss /= len(residuals) - 1
    prss.freeze()
    persistence[trial['id']] = prss


cd.shared.per_trial(df, calculate_persistence)


cd.display.markdown(
    """
    Persistent Residuals
    --------------------

    Consider a fictional trackway where two simulation trials (a and b)
    produce the following two coupling length plots:

    ![Persistent Residuals Example 1](assets/Persistence-Example-1.svg)

    Both plots have the same value everywhere but for two coupling length
    samples. The question to ask ourselves is: are these two trials
    equally efficacious as a solution for their given trackway?

    A common approach for determining this is a residual analysis, where the
    difference between each sample and the expected value is calculated. Each
    difference is squared to make all values positive and weight relatively
    larger differences more strongly than smaller ones. If we specify the
    consistent baseline value as the expectation value, we can calculate this
    residual sum of the squares (RSS) as:

    $$$
        RSS = @sum_{i=1}^{N} @left( x_i - @bar{x} @right)^2
    $$$

    where $$ @bar{x} $$ is the baseline value. For the example plots above,
    the result for these two trials is identical. A standard residual analysis
    would conclude that the two trials are equally efficacious solutions for
    their trackway.

    We can improve the residual analysis by taking into account the physical
    restrictions on the trackmaker. In trial _(a)_, the two deviating samples
    are separated samples that do not deviate. This behavior could plausibly
    have been cause by some combination of the trackmaker taking larger or
    smaller steps with its manus or pes respectively. In the subsequent sample
    where the coupling length returns to the baseline value, the trackmaker
    accounted for the previous deviation.

    The story is different for trial _(b)_. In this trial there are two
    consecutive deviations from the baseline. The first one can be explained
    as it was for trial _(a)_, but not the second. For the second deviation to
    exist, the trackmaker had to deliberately alter the movements of its other
    limbs to maintain the deviation in coupling length. The deviation could be
    accounted for by flexing the back. Another possibility is the trackmaker
    altered how much the manus and pes lead or lag relative to the body
    position. Either way, there are physical limits that prevent large
    deviations from persisting for more than a single point.

    Taking this into account requires altering the way the residuals are
    calculated. Our concern is not that a residual exists, but that a residual
    persists. We can define this mathematically by replacing the square of
    each residual in the _RSS_ calculation with the product of nearest
    neighbor residuals,

    $$$
        PRSS = @sum_{i=1}^{N-1}
            @left| x_i - @bar{x} @right|
            @left| x_{i+1} - @bar{x} @right|
    $$$

    Applied to our example from above, trial _(a)_ has $$ PRSS = 0 $$ whereas
    trial _(b)_ has a $$ PRSS = 0.023 $$. The persistent residual removes noise
    variations caused by single-sample deviations. With it we can conclude
    that trial _(a)_ is a more efficacious solution for the trackway.

    In the example above we specified a reasonable, but somewhat arbitrary
    value for the expectation value $$ @bar{x} $$. For more general simulation
    trials, the _PRSS_ is better expressed as:

    $$$
        PRSS = @sum_{i=1}^{N-1}
            @left| CL_i - @overline{CL} @right|
            @left| CL_{i+1} - @overline{CL} @right|
    $$$

    where $$ @overline{CL} $$ is the median coupling length for the simulation
    trial. Applying this _PRSS_ formulation to the BEB 500 S1 trackway yields:
    """
)

cd.display.plotly(
    data=cd.shared.create_scatter(
        df,
        [unnormalized[tid].value for tid in df.id],
        [unnormalized[tid].uncertainty for tid in df.id]
    ),
    layout=plotting.create_layout(
        {'hovermode': 'closest'},
        title='Coupling Length Persistent Residual Sum of Squares',
        x_label='Trial Index (#)',
        y_label='Persistent RSS'
    )
)

cd.display.markdown(
    """
    It is immediately apparent that there is a scaling issue in these results.
    We didn't observe it in our fictional example because the two trials shared
    the same expectation values. Median coupling values generally differ in
    actual simulation trials. Normalizing the residuals by their median
    coupling values eliminates the problem:

    $$$
        PRSS = @sum_{i=1}^{N-1}
            @left| @frac{CL_i}{@overline{CL}} - 1 @right|
            @left| @frac{CL_{i+1}}{@overline{CL}} - 1 @right|
    $$$

    There is also a more subtle issue caused by boundary conditions at the
    beginning and end of the trackway. The number of samples, _N_, in a trial
    depends on the chosen gait for that trial. For example, manus locators in
    a long-coupled trial are further ahead in a trackway than in a
    short-coupled trial at the same time in a simulation. If the end of the
    trackway doesn't include more manus prints than pes prints, the
    long-coupled trial will have fewer samples than the short-coupled one
    because the simulation will reach the end of the trackway faster. This ends
    up penalizing simulation trials with more samples. Resolving this issue is
    simply a matter of dividing the _PRSS_ by the number of residuals in the
    summation:

    $$$
        PRSS = @frac{1}{N-1} @sum_{i=1}^{N-1}
            @left| @frac{CL_i}{@overline{CL}} - 1 @right|
            @left| @frac{CL_{i+1}}{@overline{CL}} - 1 @right|
    $$$

    $$ PRSS $$ can now be calculated for every simulation trial on a
    trackway and used to compare one trial to another. For BEB 500 S1 this
    yields:
    """
)

cd.display.plotly(
    data=cd.shared.create_scatter(
        df,
        [persistence[tid].value for tid in df.id],
        [persistence[tid].uncertainty for tid in df.id]
    ),
    layout=plotting.create_layout(
        {'hovermode': 'closest'},
        title='Normalized Coupling Length Persistent Residual Sum of Squares',
        x_label='Trial Index (#)',
        y_label='Persistent RSS'
    )
)

comparisons = dict()
minimum_residual = mstats.values.minimum(persistence.values())

for key, res in persistence.items():
    comparisons[key] = abs(
        (res.value - minimum_residual.value) /
        math.sqrt(res.uncertainty ** 2 + minimum_residual.uncertainty ** 2)
    )

cd.display.markdown(
    """
    It is now possible to use $$ PRSS $$ values to compare the solution efficacy
    of one trial, _a_, with another trial, _b_:

    $$$
        @Delta_{PRSS} = @frac
            { @left| PRSS_a - PRSS_b @right| }
            { @sqrt{ @sigma_a^2 + @sigma_b^2 } }
    $$$

    where $$ @delta_{(a, b)} $$ are the uncertainties for the _a_ and _b_
    trials. This is a standard deviation formula used for comparing two values
    with uncertainties.

    While pairwise comparisons are useful, what we'd really like is a global
    comparison of all trials. This allows the solution efficacy of every trial
    to be ranked all at once. To do that we generalize the previous comparison
    formula to:

    $$$
        @Delta_{PRSS} = @frac
            { @left| PRSS_i - PRSS_{min} @right| }
            { @sqrt{ @sigma_i^2 + @sigma_{min}^{2} } }
    $$$

    Comparisons are made for each trial relative to the smallest persistent
    residual sum of the squares value, $$ PRSS_{min}, $$ from the collection
    of solutions. A value of _0_ indicates that there is no observed difference
    between a particular trial and the _"best"_ solution. Values greater than
    _0_ indicate a less efficacious solution than $$ PRSS_{min} $$. This makes
    $$ @Delta_{PRSS} $$ a suitable as a fitness parameter for persistent
    residuals.
    """
)

df['persistence'] = [comparisons[tid] for tid in df.id]
cd.display.plotly(
    data=go.Bar(
        y=df.persistence,
        text=df.short_id,
        marker=dict(
            color=df.color
        )
    ),
    layout=plotting.create_layout(
        title='PRSS Fitness',
        x_label='Trial Index (#)',
        y_label='Fitness'
    )
)

