import cauldron as cd
import measurement_stats as mstats
from cauldron import plotting

GAIT_ID = 'G2'
cd.shared.GAIT_ID = GAIT_ID


def plot_couplings(df_row, trial):
    """
    :param df_row:
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
            title='{} Coupling Length'.format(trial['short_id']),
            x_label='Cycle (#)',
            y_label='Coupling Length (m)',
            y_bounds=[median.value - 0.5, median.value + 0.5]
        )
    )

    delta = abs(min_value - max_value)
    deviation = abs(min_value.value - max_value.value) / delta.uncertainty

    cd.display.markdown(
        """
        Reference Statistics:

        * _Minimum:_ __{{ min }} m__
        * _Median:_ __{{ median }} m__
        * _Max:_ __{{ max }} m__
        * _Deviations:_ __{{ deviation }}__
        """,
        min=min_value.html_label,
        median=median.html_label,
        max=max_value.html_label,
        deviation=0.01 * round(100 * deviation)
    )
cd.shared.plot_couplings = plot_couplings

df = cd.shared.df
df = df[
    (df.gait_id == cd.shared.GAIT_ID) &
    (df.duty_cycle == 60)
].sort_values(by='coupling_length')

cd.display.header('Coupling Lengths versus Cycle', 2)
cd.display.markdown(
    """
    Let's now begin by isolating the group of trials of the {{ gait_id }} gait
    type and plotting their coupling-length values versus cycle. The following
    plots each have a one-meter y-axis interval centered around the median
    coupling length value for that trial. Summary statistics are printed below
    each plot for reference.
    """,
    gait_id=GAIT_ID
)

cd.shared.per_trial(df, plot_couplings)

cd.display.markdown(
    """
    The observed variations in coupling length values within each trial arise
    from two potential sources. The first is noise, which is inherent in any
    biological system. The second is a characteristic reflection of the
    trackmaker's physical proportions combined with its gait or gaits. It's
    this second type of characteristic variation that we will exploit.
    """
)
