import cauldron as cd
import measurement_stats as mstats

cd.display.markdown(
    """
    ## Cumulative Distribution Remainder

    To get around the problems of histogram-based analyses, we replace the
    histogram plot with a Cumulative Distribution Remainder (CDR) plot. A CDR
    plot is the continuous equivalent of a discrete histogram plot and does
    not suffer from histogram binning problems. On a CDR plot, the point (X, Y)
    is read as _“Y amount of the data that resides outside the range [0, X]”._

    The CDR equivalent of the histogram of track width deviations plotted in
    the previous step is then:
    """
)

cd.shared.plot_remainder(
    data=cd.shared.width_data,
    key='width',
    label='Width',
    is_log=False,
    normal_comparison=False
)

cdr_values = cd.shared.cdr_values_at(cd.shared.width_data, [0, 2])

cd.display.markdown(
    """
    According to the CDR plot, nearly half ({{ y0 }}%) of the tracks
    measured have no deviation between the field and map measured track
    widths. And only {{ y2 }}% of the tracks have a deviation outside of the
    200% significance threshold.

    These 200%+ deviations could either be systematic errors or random ones.
    If they are systematic errors, they might be an indicator of
    deficiencies in one measurement technique relative to the other. But that
    requires ruling out statistical random errors first and then analyzing
    what remains.

    To do that a reference line is added to the plot, which is the Gaussian,
    normal distribution CDR.
    """,
    y0=cdr_values[0]['label'],
    y2=cdr_values[2]['label']
)

cd.shared.plot_remainder(
    data=cd.shared.width_data,
    key='width',
    label='Width',
    is_log=False,
    normal_comparison=True
)

cd.display.markdown(
    """
    If one were to assume that the deviations between track measurements
    were entirely random, the CDR for the measurement deviations would
    track the Gaussian distribution. Not that the CDR values match the
    Gaussian distribution at each point, but that the area under the CDR
    curve for a given interval should equal the area under the Gaussian CDR.

    That is not the case for the track width CDR. Until a 200% deviation,
    the track width deviation CDR is well below the Gaussian reference. This
    is an indication that the two measurement techniques are effectively
    comparable for all but {{ y2 }}% of the measured tracks.

    All that remains is to investigate the tail of the CDR in the 200%+
    region to determine if there is any significance to the to that data
    that could distinguish one technique from the other.

    A semi-log plot of the CDR better displays the tail region of interest.
    """,
    y2=cdr_values[2]['label']
)

cd.shared.plot_remainder(
    data=cd.shared.width_data,
    key='width',
    label='Width',
    is_log=True
)

cd.display.markdown(
    """
    From a purely statistical perspective, the difference between the track
    width CDR and the Gaussian reference is too small to be significant
    given how much lower the CDR is than the Gaussian reference for the less
    than 200% deviation region.

    It is also easy to explain away the tail. Large deviations might be
    caused by data entry errors. There might also be differences in the
    interpretation of a track measurement between the researchers that made
    the two measurements.

    An effort was made to investigate the tracks with large deviations when
    it was possible because the tracks were preserved. It turned out that in
    each case a data entry or large measurement error was responsible for
    the large deviation.

    Given that, we can conclude that there was no unexplained significant
    difference between the field and map measurement techniques for track
    width measurements.
    """
)
