import cauldron as cd
import measurement_stats as mstats

all = cd.shared.entire_trackway
section = cd.shared.simulation_region


def compute_deviation(key):
    """

    :param key:
    :return:
    """

    a = all[key]['median']
    b = section[key]['median']

    delta = a - b
    deviation = abs((a.value - b.value) / delta.uncertainty)
    deviation = mstats.value.round_significant(deviation, 2)

    return dict(
        all=a,
        section=b,
        deviation=deviation
    )

cd.display.markdown(
    """
    Conclusions
    ===========

    A quantitative comparison between the values for the entire trackway
    and the simulation region yield no significant deviations between any
    of the values:

    Pes Width Deviation: **{{ pes_width.deviation }}**

     * Entire Trackway: {{ pes_width.all.html_label }}
     * Simulation Region: {{ pes_width.section.html_label }}

    Pes Length Deviation: **{{ pes_length.deviation }}**

     * Entire Trackway: {{ pes_length.all.html_label }}
     * Simulation Region: {{ pes_length.section.html_label }}

    Pes Aspect Deviation: **{{ pes_aspect.deviation }}**

     * Entire Trackway: {{ pes_aspect.all.html_label }}
     * Simulation Region: {{ pes_aspect.section.html_label }}

    Manus Width Deviation: **{{ manus_width.deviation }}**

     * Entire Trackway: {{ manus_width.all.html_label }}
     * Simulation Region: {{ manus_width.section.html_label }}

    Manus Length Deviation: **{{ manus_length.deviation }}**

     * Entire Trackway: {{ manus_length.all.html_label }}
     * Simulation Region: {{ manus_length.section.html_label }}

    Manus Aspect Deviation: **{{ manus_aspect.deviation }}**

     * Entire Trackway: {{ manus_aspect.all.html_label }}
     * Simulation Region: {{ manus_aspect.section.html_label }}

    The lack of significant deviation between any of the track size
    measurements indicates that the simulation region of trackway is
    indicative of the entire trackway. The choice to focus on the simulation
    region did not bias the results.
    """,
    pes_width=compute_deviation('pes_width'),
    pes_length=compute_deviation('pes_length'),
    pes_aspect=compute_deviation('pes_aspect'),
    manus_width=compute_deviation('manus_width'),
    manus_length=compute_deviation('manus_length'),
    manus_aspect=compute_deviation('manus_aspect'),
)
