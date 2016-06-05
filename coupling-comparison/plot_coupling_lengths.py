import cauldron as cd
from cauldron import plotting

trials = cd.shared.trials
traces = []

for t in trials:

    values = [x['value'] for x in t['couplings']['lengths']]
    uncertainties = [x['uncertainty'] for x in t['couplings']['lengths']]

    plot = plotting.make_line_data(
        x=t['times']['cycles'],
        y=values,
        y_unc=uncertainties,
        name=t['settings']['id'],
        color=plotting.get_color(trials.index(t), 0.8),
        fill_color=plotting.get_color(trials.index(t), 0.2)
    )
    traces += plot['data']

cd.display.plotly(
    data=traces,
    layout=plotting.create_layout(
        title='Coupling Length Comparison',
        x_label='Cycle (#)',
        y_label='Coupling Length (m)'
    ),
    scale=0.8
)

