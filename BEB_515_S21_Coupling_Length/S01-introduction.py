import cauldron as cd
from cauldron import plotting

cd.shared.trackway_name = 'BEB 515 S21'

cd.display.markdown(
    """
    # {{ name }}

    A comparative investigation of gait simulation trials on the {{ name }}
    trackway using coupling lengths to determine the efficacy of each possible
    solution. The following diagram is a schematic representation of the
    section of {{ name }} analyzed here.

    ![{{ name }} Trackway](assets/trackway.svg)

    Throughout this investigation we'll be making comparisons between a number
    of different simulation trials. The per-gait color scheme shown below will
    be used when plotting per-trial results for comparison.
    """,
    name=cd.shared.trackway_name
)

template = """
    <div style="margin:0.5em;display:flex;flex-direction:column;">
        <div style="width:50px;height:40px;background-color:{color};">
        </div>
        <div style="width:100%;text-align:center">G{index}</div>
    </div>
    """

swatches = []
for i in range(8):
    swatches.append(template.format(
        index=i,
        color=plotting.get_color(i)
    ))

cd.display.html(
    """
    <div style="display:flex;align-items:middle;justify-content:center;">
        {swatches}
    </div>
    """.format(
        swatches=''.join(swatches)
    )
)

cd.display.markdown(
    """
    The following table outlines the simulation trials run on the {{ name }}
    trackway. Gaits are uniquely identified in terms of their gait identifier,
    separation and duty cycle values. The table has been sorted by median
    coupling lengths for each trial.
    """,
    name=cd.shared.trackway_name
)
