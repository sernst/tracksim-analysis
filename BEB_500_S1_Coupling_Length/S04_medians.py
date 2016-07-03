import cauldron as cd
import pandas as pd
import plotly.graph_objs as go
from cauldron import plotting

df = cd.shared.df  # type: pd.DataFrame

cd.display.header('Median Coupling Lengths')

cd.display.plotly(
    data=cd.shared.create_scatter(df, 'coupling_length', 'uncertainty'),
    layout=plotting.create_layout(
        title='Median Coupling Lengths by Trial',
        x_label='Trial Index (#)',
        y_label='Coupling Length (m)'
    )
)

cd.display.markdown(
    """
    Despite the high-quality of preservation of this trackway, there is
    a large amount of overlap between median coupling length values in
    neighboring solutions. There is very little information that the median
    values explicitly provide. The trends in fractional uncertainty among the
    trials complicates things further.
    """
)

cd.display.plotly(
    data=go.Bar(
        y=100.0 * df.relative_uncertainty,
        text=df.short_id,
        marker=dict(
            color=df.color
        )
    ),
    layout=plotting.create_layout(
        title='Relative Coupling Length Uncertainties',
        x_label='Trial Index (#)',
        y_label='Relative Uncertainty (%)'
    )
)


cd.display.markdown(
    """
    The fractional uncertainties do not scale with the median coupling length
    values. Shorter trials have a greater relative uncertainty than their
    longer counterparts.

    There are also no trends within either of these plots that could be used to
    determine the relative efficacy of particular solutions or regions. The
    development of quality-of-fit parameters from the coupling length data may
    be more fruitful.
    """
)
