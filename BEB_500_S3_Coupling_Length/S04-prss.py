import cauldron as cd
import plotly.graph_objs as go
from cauldron import plotting
from tracksim.coupling import prss
from tracksim.coupling.plotting import scatter

cd.watch(prss)

cd.display.markdown(
    """
    ## Persistent Residuals (PRSS)
    """
)

df = cd.shared.df
data = prss.compute_many(cd.shared.trials)
fitness = prss.to_fitness(data['prss_norm'])
df['persistence'] = [fitness[tid] for tid in df.id]

cd.display.plotly(
    data=scatter.create(
        data_frame=df,
        value_column=[data['prss'][tid].value for tid in df.id],
        uncertainty_column=[data['prss'][tid].uncertainty for tid in df.id],
        x_column='order'
    ),
    layout=plotting.create_layout(
        {'hovermode': 'closest'},
        title='Coupling Length Persistent Residual Sum of Squares',
        x_label='Trial Index (#)',
        y_label='Persistent RSS'
    )
)

cd.display.plotly(
    data=scatter.create(
        df,
        [data['prss_norm'][tid].value for tid in df.id],
        [data['prss_norm'][tid].uncertainty for tid in df.id],
        x_column='order'
    ),
    layout=plotting.create_layout(
        {'hovermode': 'closest'},
        title='Normalized Coupling Length Persistent Residual Sum of Squares',
        x_label='Trial Index (#)',
        y_label='Persistent RSS'
    )
)

cd.display.plotly(
    data=go.Bar(
        y=df.persistence,
        text=df.short_id,
        marker=dict(
            color=df.color
        )
    ),
    layout=plotting.create_layout(
        title='PRSS Fitness',
        x_label='Trial Index (#)',
        y_label='Fitness'
    )
)

