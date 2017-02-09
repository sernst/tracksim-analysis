import cauldron as cd

from _Gauge_Quantization import generator
from _Gauge_Quantization.windowing import display
from _Gauge_Quantization.generator import draw

tracks = generator.create(12, (4, 0.3, 0.000001), (8, 0.1, 0.000001))
tracks['width'] = 0.3

cd.display.markdown(
    """
    # A Shrinking Gauge

    The first idealized trackway is a shrinking gauge from a larger to smaller
    value. There is an initially constant gauge region. This constant region is
    followed by a transition region from the larger to smaller gauge value. The
    trackway then remains at the small gauge until it ends. For numerical
    simplicity we define the stride length to be a constant 2 meters and a
    _track phase_ of 50%. This places each track at an integer meter value and
    allows us to refer to tracks by a 1-indexed value that also corresponds
    to their position within the trackway.

    The trackway diagram looks like:
    """
)

cd.display.svg(draw.draw_tracks(tracks))

cd.display.markdown(
    """
    We can fairly easily cluster the beginning and ending regions of the
    trackway given that they are distinct and constant. How we deal with the
    gauge values in the transition region is not so clear. In order to compute
    clustered gauge segments for a general trackway we need to specify a
    tolerance limit for the comparison operation. If the difference between the
    median gauge value for clustered segment and a comparison track's gauge
    exceeds the tolerance the clustered segment ends and the comparison track's
    gauge is used to create a new cluster.

    But how do we determine the appropriate tolerance? While there is no
    completely objective way to do this, a standard approach is to find a
    characteristic length specific to the system. A good choice for the
    characteristic length reduces the arbitrariness of the tolerance as long
    as it can be used reliably and broadly. We will use the median track width
    for our characteristic length. For our example case, we will assign a value
    of 30cm as the median track width.

    Running the algorithm first using a tolerance value of
    $$ 1w = 30cm $$ yields the following gauge clustering:
    """
)

result = display.compute_unweighted(tracks, 1.0)
cd.display.plotly(
    data=result['data'],
    layout=dict(
        title='Segmented Gauges (tolerance 1w)',
        **result['layout']
    )
)

cd.display.markdown(
    """
    There's only one segment for the entire trackway because the tolerance
    value is large relative to the amount of change in gauge along the
    trackway. If we instead use a tolerance of $$ 0.5w = 15cm $$ we get a
    different result:
    """
)

result = display.compute_unweighted(tracks, 0.5)
cd.display.plotly(
    data=result['data'],
    layout=dict(
        title='Segmented Gauges (tolerance 0.5w)',
        **result['layout']
    )
)

cd.display.markdown(
    """
    With the reduced tolerance we've resolved the two distinct regions at the
    ends, but they are not symmetric. Why does track 6 appear in the second
    region instead of the first? The answer is that it is a consequence of
    the use of a forward windowing algorithm. The first segment has a
    sufficiently low variance when it reaches the sixth track that the
    comparison rejects it. The sixth track then starts a new segment, which
    quickly reaches a higher variance because the region is initially populated
    with the transitioning gauge values.

    If we were to run this same trackway with a reverse windowing algorithm
    under the same conditions we would get a different result. In that case
    the sixth track would be in the first segment instead of the second one
    and the first segment would have the larger variance caused by its
    conception within the transition region. The only reason to select one
    method over the other is to prefer an algorithm that preferences the
    direction of travel of the trackmaker. While this makes the choice less
    arbitrary, it is also not entirely without bias.

    And perhaps two regions is unsatisfying and the bulk of the transition
    region shouldn't be included in the end segments. We can always change
    the tolerance again. For a value of $$ 0.25w = 7.5cm $$ we get:
    """
)

result = display.compute_unweighted(tracks, 0.25)
cd.display.plotly(
    data=result['data'],
    layout=dict(
        title='Segmented Gauges (tolerance 0.25w)',
        **result['layout']
    )
)

cd.display.markdown(
    """
    This tolerance produces four regions instead of three. Should we adjust
    again and try to find the goldilocks solution? The answer is absolutely
    not. We've exposed where the arbitrariness is within this technique.

    It is also not limited to an idea case. We find similar issues when applied
    to real trackway data as well.
    """
)
