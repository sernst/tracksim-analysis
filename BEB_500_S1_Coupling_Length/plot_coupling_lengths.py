import cauldron as cd
import measurement_stats as mstats
from cauldron import plotting

GAIT_ID = 'G2'
cd.shared.GAIT_ID = GAIT_ID


def plot_couplings(trial):
    """

    :param trial:
    :return:
    """

    data = trial['couplings']['lengths']
    median = mstats.ValueUncertainty(**trial['couplings']['value'])

    couplings = mstats.values.from_serialized(
        [v['value'] for v in data]
    )
    min_value = mstats.values.minimum(couplings)
    max_value = mstats.values.maximum(couplings)

    y, unc = mstats.values.unzip(couplings)

    plot = plotting.make_line_data(
        x=[v['time'] for v in data],
        y=y,
        y_unc=unc,
        color=plotting.get_color(int(trial['id'][1]), 0.8),
        fill_color=plotting.get_color(int(trial['id'][1]), 0.3)
    )

    cd.display.plotly(
        data=plot['data'],
        layout=plotting.create_layout(
            dict(
                showlegend=False
            ),
            title='{} Coupling Length'.format(
                trial['id'].split('_', 1)[0]
            ),
            x_label='Cycle (#)',
            y_label='Coupling Length (m)',
            y_bounds=[median.value - 0.5, median.value + 0.5]
        )
    )

    deviation = 100.0 * (max_value - min_value) / median
    cd.display.markdown(
        """
        Reference Statistics:

        * _Minimum:_ __{{ min }} m__
        * _Median:_ __{{ median }} m__
        * _Max:_ __{{ max }} m__
        * _Swing:_ __{{ swing }}%__
        """,
        min=min_value.html_label,
        median=median.html_label,
        max=max_value.html_label,
        swing=deviation.html_label
    )


df = cd.shared.df
df = df[df.gait_id == cd.shared.GAIT_ID].sort_values(by='coupling_length')

cd.display.header('Coupling Lengths versus Cycle', 2)
cd.display.markdown(
    """
    Let's now begin by isolating the group of trials of the {{ gait_id }} gait
    type and plotting their coupling-length values versus cycle. The y-axis in
    the following plots both have a one meter interval that is centered around
    the median coupling length value for that trial to make comparison between
    them easier. Summary statistics about each plot are printed below them for
    reference.
    """,
    gait_id=GAIT_ID
)

cd.shared.per_trial(df, plot_couplings)

cd.display.markdown(
    """
    It is clear that the coupling length behaves differently over the course of
    each trial. Given that these differences are not reflected by the
    corresponding reference statistics - they are very similar between trials
    when scaling is considered - the need for transient-focused analysis is
    even more apparent than before.
    """
)
