import cauldron as cd

cd.display.markdown(
    """
    To begin with, we’ve replaced histograms with Cumulative Distribution
    Remainder (CDR) plots. A CDR plot is the continuous equivalent of a
    discrete histogram plot and does not suffer from binning problems. On a
    CDR plot, the point (X, Y) is read as “Y amount of the data resides
    outside the range [0, X]”. In Figure 9 the value of approximately
    (150%, 10%), for example, would read as “10% of the data values are greater
    than 150%”. Just as with the previous histograms (Figure 7), the CDR
    function is expected to decay given that fewer values in the dataset
    should exist at larger deviations. In both Figures 9 and 10 the CDR plots
    begin below 60%, which indicates that more than 40% of the data have no
    deviation from what is expected if distributed normally.  This fact is
    made apparent in a CDR but not in a conventional histogram.  If one were
    to assume that deviations between width and length measurements in the
    catalog and sitemaps were random, the CDR functions in Figure 9 and 10
    should behave identically to a Normal Gaussian distribution.  The black
    dashed lines in each of Figures 9 and 10 are Gaussian CDR reference lines.
    Wherever the CDR plots lie below the Gaussian reference line, the
    measurement deviations are smaller than a random statistical prediction
    would suggest, and conversely for where the CDR plots are above the
    Gaussian reference line.
    """
)

cd.shared.plot_remainder(
    data=cd.shared.width_data,
    key='width',
    label='Width',
    is_log=False
)

cd.shared.plot_remainder(
    data=cd.shared.width_data,
    key='width',
    label='Width',
    is_log=True
)
