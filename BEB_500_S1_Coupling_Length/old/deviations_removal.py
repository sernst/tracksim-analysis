import cauldron as cd
from cauldron import plotting
import pandas as pd
from plotly import graph_objs as go

max_deviation_values = []
max_deviation_indexes = []
max_coupling_deviations = dict()


def index_of_max_deviation(df_row, trial):
    """
    :param df_row:
    :param trial:
    :return:
    """

    deviations = cd.shared.deviations[trial['id']]
    max_value = max(cd.shared.deviations[trial['id']])
    max_deviation_values.append(max_value)

    max_index = [i for i, dev in enumerate(deviations) if dev == max_value]
    max_deviation_indexes.append(max_index[0])

    max_coupling_deviation = trial['couplings']['lengths'][max_index[0]]
    max_coupling_deviations[trial['id']] = max_coupling_deviation

df = cd.shared.df  # type: pd.DataFrame
cd.shared.per_trial(df, index_of_max_deviation)
df['deviation'] = max_deviation_values
df['deviation_index'] = max_deviation_indexes

cd.display.plotly(
    data=go.Bar(
        y=100 * (df.deviation * df.uncertainty) / df.coupling_length,
        text=df.short_id,
        marker=dict(
            color=df.color
        )
    ),
    layout=plotting.create_layout(
        title='Fractional Maximum Median Deviations',
        x_label='Trial Index (#)',
        y_label='Fractional Deviation (%)'
    )
)

df_remaining = df[df.deviation <= 2.05]
cd.display.markdown(
    """
    This reduces the set of possible solutions from {{ total }} to
    {{ remaining }}. Notably, all of the trials with a separation of 2
    were removed from the possible solution set. The median coupling
    lengths of the remaining trials are now:
    """,
    total=df.shape[0],
    remaining=df_remaining.shape[0]
)

cd.display.plotly(
    data=cd.shared.create_scatter(
        df_remaining, 'coupling_length', 'uncertainty'
    ),
    layout=plotting.create_layout(
        title='Median Coupling Lengths by Trial',
        x_label='Trial Index (#)',
        y_label='Coupling Length (m)'
    )
)

cd.shared.df_remaining = df_remaining
