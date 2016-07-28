import math

import numpy as np
from plotly import graph_objs as go
import cauldron as cd
from cauldron import plotting
import pandas as pd

df = cd.shared.df  # type: pd.DataFrame

entries = []
traces = []

for gid in df.label.unique():

    df_sub = df[df.label == gid]

    traces.append(go.Box(
        y=df_sub.fitness,
        name=gid,
        marker={
            'color': df_sub.iloc[0].color
        }
    ))

    entries.append(dict(
        label=gid,
        fitness=np.median(df_sub.fitness),
        coupling_length=np.median(df_sub.coupling_length),
        color=df_sub.iloc[0].color
    ))

df = pd.DataFrame(entries).sort_values(by='coupling_length')

cd.display.plotly(
    data=go.Bar(
        y=df.fitness,
        text=df.label,
        marker=dict(
            color=df.color
        )
    ),
    layout=plotting.create_layout(
        title='Solution Fitness',
        x_label='Trial Index (#)',
        y_label='Fitness (%)'
    )
)

cd.display.plotly(
    data=traces,
    layout=plotting.create_layout(
        title='Solution Fitness',
        x_label='Trial Index (#)',
        y_label='Fitness (%)'
    )
)
