import math

import cauldron as cd
from cauldron import plotting
import measurement_stats as mstats
import plotly.graph_objs as go

persistent_residuals = dict()
unexplained = dict()


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

    residuals = [abs(cl / median.value - 1) for cl in couplings]
    residual_max = mstats.values.maximum(residuals)
    residuals = [r / residual_max.value for r in residuals]

    out = mstats.ValueUncertainty(0, 0.00001)
    for index, res in enumerate(residuals[:-2]):
        # out = max(out, res * sum(residuals[index + 1: index + 3]))
        out = mstats.value.maximum(out, res * residuals[index + 1])

    persistent_residuals[trial['id']] = out
    unexplained[trial['id']] = 100 * math.sqrt(
        max(0, out.value - out.uncertainty) / (len(residuals) - 1)
    )


df = cd.shared.df
cd.shared.per_trial(df, calculate_residuals)

cd.display.plotly(
    data=cd.shared.create_scatter(
        df,
        [persistent_residuals[tid].value for tid in df.id],
        [persistent_residuals[tid].uncertainty for tid in df.id]
    ),
    layout=plotting.create_layout(
        {'hovermode': 'closest'},
        title='Coupling Length Persistent Residual Sum of Squares',
        x_label='Trial Index (#)',
        y_label='Persistent RSS'
    )
)

values = [unexplained[tid] for tid in df.id]
df['persistence'] = values

cd.display.plotly(
    data=go.Bar(
        y=values,
        text=df.short_id,
        marker=dict(
            color=df.color
        )
    ),
    layout=plotting.create_layout(
        title='Unexplained Normalized Coupling Length Persistent RMSD',
        x_label='Trial Index (#)',
        y_label='Unexplained PRMSD (%)'
    )
)
