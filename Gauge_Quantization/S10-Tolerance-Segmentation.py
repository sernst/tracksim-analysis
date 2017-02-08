import cauldron as cd
import pandas as pd

from _Gauge_Quantization.windowing import display

tracks = cd.shared.tracks  # type: pd.DataFrame
trackway_name = cd.shared.TRACKWAY_NAME

cd.display.markdown(
    """
    # Segmentation of {{ trackway_name }}

    Applying the same technique to {{ trackway_name }} that we did to the
    idealized shrinking gauge trackway above, we can see that the choice of
    tolerance still has a large influence on the segmentation.
    """,
    trackway_name=trackway_name
)

result = display.compute_unweighted(tracks, 1)
cd.display.plotly(
    data=result['data'],
    layout=dict(
        title='{} Segmented Gauges (tolerance 1w)'.format(trackway_name),
        **result['layout']
    )
)

result = display.compute_unweighted(tracks, 0.5)
cd.display.plotly(
    data=result['data'],
    layout=dict(
        title='{} Segmented Gauges (tolerance 0.5w)'.format(trackway_name),
        **result['layout']
    )
)

result = display.compute_unweighted(tracks, 0.25)
cd.display.plotly(
    data=result['data'],
    layout=dict(
        title='{} Segmented Gauges (tolerance 0.25w)'.format(trackway_name),
        **result['layout']
    )
)

cd.display.markdown(
    """
    There are a number of things we can do to make this analysis more
    scientifically robust.
    """
)
