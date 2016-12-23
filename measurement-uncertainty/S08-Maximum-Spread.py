import cauldron as cd
from cauldron import plotting
from plotly import graph_objs as go
import measurement_stats as mstats
import numpy as np

trackways_df = cd.shared.trackways_df

cd.display.markdown(
    """
    ## Maximum Spreads

    It would be easy to assume that there is a correlation between high width
    spreads and high length spreads. However, plotting them against each other
    reveals a very weak correlation.
    """
)

cd.display.plotly(
    data=go.Scatter(
        x=trackways_df['length_spread'],
        y=trackways_df['width_spread'],
        mode='markers',
        marker=dict(
            color=plotting.get_color(2)
        ),
        text=trackways_df['trackway']
    ),
    layout=plotting.create_layout(
        {'hovermode': 'closest'},
        title='Width versus Length Spreads Per Trackway',
        x_label='Length Spreads (%)',
        y_label='Width Spreads (%)'
    )
)

cd.display.markdown(
    """
    Looking at maximum spreads, we get a median value of {{ median }}%,
    which is larger than either the length or the width values.

    This fact, combined by the lack of strong correlation, means that we
    should not be classifying trackways by their length or width spreads,
    but by whichever one of the two has the maximum spread value.

    The distribution of maximum spreads looks like:
    """,
    median=mstats.value.round_to_order(
        value=np.median(trackways_df['max_spread'].values),
        order=0
    )
)

cd.display.plotly(
    data=go.Histogram(
        x=trackways_df['max_spread'],
        marker=dict(
            color=plotting.get_color(2)
        )
    ),
    layout=plotting.create_layout(
        title='Maximum Spread Distribution by Trackway',
        x_label='Relative Uncertainty Spread (%)',
        y_label='Frequency (#)',
    )
)
