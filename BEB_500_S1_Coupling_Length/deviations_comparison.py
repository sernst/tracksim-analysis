import pandas as pd
import cauldron as cd
from cauldron import plotting
from plotly import graph_objs as go
import measurement_stats as mstats

df = cd.shared.df  # type: pd.DataFrame
deviations = dict()


def calculate_deviations(trial):
    """

    :param trial:
    :return:
    """

    median = mstats.ValueUncertainty(**trial['couplings']['value'])
    couplings = mstats.values.from_serialized(
        [cl['value'] for cl in trial['couplings']['lengths']]
    )

    deviations[trial['id']] = [
        abs(cl.value - median.value) / cl.uncertainty
        for cl in couplings
    ]

cd.shared.per_trial(df, calculate_deviations)

max_deviations = [max(deviations[tid]) for tid in df.id]
colors = [plotting.get_color(int(tid[1])) for tid in df.id]

cd.display.plotly(
    data=go.Bar(
        y=max_deviations,
        text=df.id,
        marker=dict(
            color=colors
        )
    ),
    layout=plotting.create_layout(
        title='Fractional Median Deviations',
        x_label='Trial Index (#)',
        y_label='Fractional Deviation'
    )
)

cd.display.header('Median Deviations For Every Trial')
cd.shared.per_trial(
    df,
    cd.shared.plot_median_deviations
)
