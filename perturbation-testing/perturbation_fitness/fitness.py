import math

from plotly import graph_objs as go
import cauldron as cd
from cauldron import plotting
import pandas as pd

df = cd.shared.df  # type: pd.DataFrame

fitness = []

for index, row in df.iterrows():
    fitness.append(math.sqrt(row.rmsd ** 2 + row.swing ** 2))

fmax = max(fitness)
fmin = min(fitness)

# fitness = [(f - fmin) / fmax for f in fitness]
fitness = [f / math.sqrt(2) for f in fitness]

df['fitness'] = fitness

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
