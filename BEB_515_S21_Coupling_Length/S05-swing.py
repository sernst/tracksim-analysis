import cauldron as cd
import plotly.graph_objs as go
from cauldron import plotting
from tracksim.coupling import swing
from tracksim.coupling.plotting import scatter

cd.refresh(swing)

df = cd.shared.df
swing_data = swing.compute_many(cd.shared.trials)
fitness = swing.to_fitness(swing_data)
df['swing'] = [fitness[tid] for tid in df.id]

cd.display.plotly(
    data=scatter.create(
        df,
        [swing_data[tid].value for tid in df.id],
        [swing_data[tid].uncertainty for tid in df.id],
        x_column='order'
    ),
    layout=plotting.create_layout(
        title='Normalized Swing by Trial',
        x_label='Trial Index (#)',
        y_label='Swing'
    )
)

cd.display.plotly(
    data=go.Bar(
        y=df.swing,
        text=df.short_id,
        marker=dict(
            color=df.color
        )
    ),
    layout=plotting.create_layout(
        title='Swing Deviation',
        x_label='Trial Index (#)',
        y_label='Fractional Deviation'
    )
)

