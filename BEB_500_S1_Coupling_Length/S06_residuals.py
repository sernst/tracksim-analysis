import math

import cauldron as cd
from cauldron import plotting
import measurement_stats as mstats
from plotly import graph_objs as go

df = cd.shared.df
raw_residuals = dict()
scaled_residuals = dict()
unexplained_residuals = dict()


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

    r = sum([abs(cl - median.value) ** 2 for cl in couplings])
    scaled = sum([abs(cl / median.value - 1) ** 2 for cl in couplings])

    raw_residuals[trial['id']] = r
    scaled_residuals[trial['id']] = scaled
    unexplained_residuals[trial['id']] = 100 * math.sqrt(
        max(0, scaled.value - scaled.uncertainty) / len(couplings)
    )


cd.shared.per_trial(df, calculate_residuals)


cd.display.header('Residual Sum of Squares', 2)
cd.display.markdown(
    """
    While the individual plots can be explored and described, we seek a
    quantitatively robust and reliable way of determining the quality of fit
    for each one in order to eliminate trials from the list of possible
    solutions.

    The residual sum of the squares is a reliable method for determining the
    quality of fit between a data set and its expectation value and is defined
    as,

    $$$
        RSS = @sum_{i=1}^{N} @left( x_i - @bar{x} @right)^2
    $$$

    In this case the individual values, $$x_i$$, are the coupling length
    samples and the expectation value, $$@bar{x}$$, is the median coupling
    length for the simulation trial.

    $$$
        RSS = @sum_{i=1}^{N} @left( CL_i - CL_{median} @right)^2
    $$$

    This value can be calculated for each trial and used for comparison.
    """
)

cd.display.plotly(
    data=cd.shared.create_scatter(
        df,
        [raw_residuals[tid].value for tid in df.id],
        [raw_residuals[tid].uncertainty for tid in df.id]
    ),
    layout=plotting.create_layout(
        {'hovermode': 'closest'},
        title='Coupling Length Residual Sum of Squares',
        x_label='Trial Index (#)',
        y_label='Residual Sum of Squares'
    )
)

cd.display.markdown(
    """
    There is an artifact of scale in the results shown above. A deviation of
    0.1m should be weighted less for a trackmaker with a coupling length of
    3m than for one with a coupling length of 1m. To fix the problem each
    trial is normalized by its median coupling length, which results in an
    updated RSS formulation,

    $$$
        RSS = @sum_{i=1}^{N} @left( @frac{CL_i}{CL_{median}} - 1 @right)^2
    $$$
    """
)

cd.display.plotly(
    data=cd.shared.create_scatter(
        df,
        [scaled_residuals[tid].value for tid in df.id],
        [scaled_residuals[tid].uncertainty for tid in df.id]
    ),
    layout=plotting.create_layout(
        {'hovermode': 'closest'},
        title='Normalized Coupling Length RSS',
        x_label='Trial Index (#)',
        y_label='Residual Sum of Squares'
    )
)

cd.display.markdown(
    """
    It is also useful to remove any residuals that can be explained by an
    understood and quantifiable reason. The uncertainty in the residual data,
    which was calculated from the original uncertainties in the trackway
    measurements is explainable and should be subtracted from the RSS, which
    yields:

    $$$
        RSS_{unexplained} =
            @sum_{i=1}^{N} @left( @frac{CL_i}{CL_{median}} - 1 @right)^2 -
            @frac{2}{CL_{median}}
            @left( @frac{CL_i}{CL_{median}} - 1 @right)
            @delta_i
    $$$

    Here $$@delta_i$$ is the uncertainty in the coupling length sample
    $$CL_i$$. It is also common to display the root-mean-square deviation
    as a percent, instead of the RSS, which can be calculated from the RSS
    above as,

    $$$
        @Delta_{RMSD} = @sqrt{
            @frac   {RSS_{unexplained}}
                    {N}
        }
    $$$
    """
)

df['rmsd'] = [unexplained_residuals[tid] for tid in df.id]
cd.display.plotly(
    data=go.Bar(
        y=df.rmsd,
        text=df.short_id,
        marker=dict(
            color=df.color
        )
    ),
    layout=plotting.create_layout(
        title='Unexplained Normalized Coupling Length RMSD',
        x_label='Trial Index (#)',
        y_label='Unexplained RMSD (%)'
    )
)

cd.display.markdown(
    """
    These RMSD value can be considered an indicator of the quality of a
    particular solution for the trackway. It is not good practice to rely on
    a single fitness parameter, even a reliable one like RMSD, when analyzing
    the viability of each trial.
    """
)
