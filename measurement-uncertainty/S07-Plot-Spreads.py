import cauldron as cd
import measurement_stats as mstats
import numpy as np
from cauldron import plotting
from plotly import graph_objs as go

trackways_df = cd.shared.trackways_df

cd.display.markdown(
    """
    ## Width Spreads

    The distribution of width spreads in the A16 database has a median spread
    value of {{ median }}%. The distribution looks like:
    """,
    median=mstats.value.round_to_order(
        value=np.median(trackways_df['width_spread'].values),
        order=0
    )
)

cd.display.plotly(
    data=go.Histogram(x=trackways_df['width_spread']),
    layout=plotting.create_layout(
        title='Width Spread Distribution by Trackway',
        x_label='Relative Uncertainty Spread (%)',
        y_label='Frequency (#)'
    )
)

cd.display.markdown(
    """
    ## Length Spreads

    The length spreads in the A16 database has a larger median spread value of
    {{ median }}%. Its distribution looks like:
    """,
    median=mstats.value.round_to_order(
        value=np.median(trackways_df['length_spread'].values),
        order=0
    )
)

cd.display.plotly(
    data=go.Histogram(
        x=trackways_df['length_spread'],
        marker=dict(
            color=plotting.get_color(1)
        )
    ),
    layout=plotting.create_layout(
        title='Length Spread Distribution by Trackway',
        x_label='Relative Uncertainty Spread (%)',
        y_label='Frequency (#)'
    )
)

