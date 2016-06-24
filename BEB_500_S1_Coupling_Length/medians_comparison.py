import pandas as pd
import cauldron as cd
from cauldron import plotting
import plotly.graph_objs as go

df = cd.shared.df  # type: pd.DataFrame

df['variance'] = 100.0 * df.uncertainty / df.coupling_length

traces = []

for index, gait_id in enumerate(sorted(df.gait_id.unique())):
    df_slice = df[df.gait_id == gait_id]
    df_slice = df_slice.sort_values(by='separation')

    traces.append(go.Scatter(
        x=df_slice.order,
        y=df_slice.coupling_length,
        error_y={
            'visible': True,
            'value': df_slice.uncertainty
        },
        mode='markers',
        marker={
            'size': 6,
            'color': plotting.get_color(index, 0.7)
        },
        text=df_slice.id,
        name=gait_id
    ))

cd.display.plotly(
    data=traces,
    layout=plotting.create_layout(
        {'hovermode': 'closest'},
        title='BEB 500 S1 Coupling Lengths',
        x_label='Trial Index (#)',
        y_label='Coupling Length (m)'
    )
)

cd.display.plotly(
    data=go.Bar(
        y=df.variance,
        text=df.id
    ),
    layout=plotting.create_layout(
        title='Fractional Coupling Length Uncertainties',
        x_label='Trial Index (#)',
        y_label='Fractional Uncertainty (%)'
    )
)
