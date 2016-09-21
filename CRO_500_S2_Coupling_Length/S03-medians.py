import cauldron as cd
import pandas as pd
import plotly.graph_objs as go
from cauldron import plotting
from tracksim.coupling.plotting import scatter

cd.refresh(scatter)

df = cd.shared.df  # type: pd.DataFrame

cd.display.markdown(
    """
    ## Median Coupling Lengths

    The median coupling length values, and their uncertainties, for each
    simulation are shown below ordered from smallest to largest.
    """
)

cd.display.plotly(
    data=scatter.create(df, 'coupling_length', 'uncertainty', 'order'),
    layout=plotting.create_layout(
        title='Median Coupling Lengths by Trial',
        x_label='Trial Index (#)',
        y_label='Coupling Length (m)'
    )
)

cd.display.markdown(
    """
    The uncertainties in the simulation trials do not scale with coupling
    length. Smaller coupling length trials generally have larger relative
    uncertainties than the larger coupling length trials:
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

