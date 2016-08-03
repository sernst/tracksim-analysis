import cauldron as cd

cd.display.markdown(
    """
    Characteristic Variations
    -------------------------

    We seek to establish parameters derived from the coupling lengths in each
    trial that can be used to quantify the characteristic variations between
    trials. These parameters will form a feature space that can be used to
    determine the fitness of each simulation trial as a solution for the
    trackway.

    As with many complex systems, the characteristic variations are
    not perfectly orthogonal to the noise. A feature space cannot be created
    that represents only the characteristic variations within trials. Some
    amount of noise will be included in each parameter and will have to be
    accounted for in the analysis.
    """
)
