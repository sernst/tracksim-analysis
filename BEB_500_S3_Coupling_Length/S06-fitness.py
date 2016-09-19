import cauldron as cd
import pandas as pd
from cauldron import plotting
from plotly import graph_objs as go
from tracksim import coupling
from tracksim.coupling.plotting import stem

cd.watch(coupling)
cd.watch(stem)

df = cd.shared.df  # type: pd.DataFrame

cd.display.header('Solution Fitness')

traces = []
for gait_id in df.gait_id.unique():
    df_slice = df[df.gait_id == gait_id]
    traces.append(go.Scatter(
        x=df_slice['persistence'],
        y=df_slice['swing'],
        mode='markers',
        marker={
            'size': 8,
            'color': df_slice.iloc[0].color
        },
        name=gait_id,
        text=df_slice.short_id
    ))

cd.display.plotly(
    data=traces,
    layout=plotting.create_layout(
        {'hovermode': 'closest'},
        title='Fitness Parameters',
        x_label='PRSS Fitness',
        y_label='Swing Fitness'
    )
)

df['fitness'] = coupling.compute_fitness_rankings(df)

cd.display.plotly(
    stem.create(df, df['fitness']),
    layout=plotting.create_layout(
        title='Solution Fitness',
        x_label='Coupling Length (m)',
        y_label='Fitness'
    )
)


