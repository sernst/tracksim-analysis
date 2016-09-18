import cauldron as cd

cd.display.markdown(
    """
    ## Length Comparisons

    We repeat the same CDR analysis carried out for track widths now for
    track lengths. The track width deviation CDR plot, with Gaussian
    reference, is:
    """
)

cd.shared.plot_remainder(
    data=cd.shared.length_data,
    key='length',
    label='Length',
    is_log=False
)

cdr_values = cd.shared.cdr_values_at(cd.shared.length_data, [0, 2])

cd.display.markdown(
    """
    The track length deviations CDR is similar in behavior to the previous
    track width deviations CDR. In this case fewer ({{ y0 }}%) tracks had no
    deviation between the two measurement methods. This is still a substantial
    amount and well below the Gaussian reference threshold. The amount of
    tracks within the 200% significance threshold ({{ y2 }}%) is also slightly
    lower than track widths.

    These differences are not large enough to come to a different conclusion
    than was reached for the track width measurements. Once again, the two
    techniques produce comparable results.
    """,
    y0=cdr_values[0]['label'],
    y2=cdr_values[2]['label']
)

cd.shared.plot_remainder(
    data=cd.shared.length_data,
    key='length',
    label='Length',
    is_log=True
)

cd.display.markdown(
    """
    We believe that the larger tail for the track length deviations is caused
    in part by the length measurements being less well defined in cases where
    the trackmaker's limb skid while making the track. In such cases, the
    length is open to greater interpretation.

    Most of the tracks in the A16 data set had little or no length skidding,
    but the potential for this kind of issue is a good reason to use track
    widths instead of track lengths as the reference measurement for scaling
    calculations.
    """
)
