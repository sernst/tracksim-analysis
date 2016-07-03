import cauldron as cd
import pandas as pd
from cauldron import plotting
from plotly import graph_objs as go

cd.display.header('Deviation Comparisons')
cd.display.markdown(
    """
    We compute these median deviations for each trial and plot the maximum
    deviation of each trial for comparison. The trials remain ordered from
    shortest to longest median coupling lengths.
    """
)

df = cd.shared.df  # type: pd.DataFrame
df['deviation'] = [max(cd.shared.deviations[tid]) for tid in df.id]

cd.display.plotly(
    data=go.Bar(
        y=df.deviation,
        text=df.short_id,
        marker=dict(
            color=df.color
        )
    ),
    layout=plotting.create_layout(
        title='Fractional Median Deviations',
        x_label='Trial Index (#)',
        y_label='Fractional Deviation'
    )
)

cd.display.markdown(
    """
    A number of tested gaits have significant deviations from the median
    value. This implies either that the trackmaker's coupling length changed
    due to flexing, or that the trackmaker switched between gaits during
    transit. Either is possible, but we will limit ourselves to searching
    for single-gait solutions.

    Every trial with a maximum deviation greater than 2 is a candidate for
    removal from our solution space if it requires flexing beyond the
    estimated limits of the trackmaker.

    """
)


