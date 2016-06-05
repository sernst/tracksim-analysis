import cauldron as cd
from cauldron import plotting

trial = cd.shared.trial
time = trial['times']['cycles']
couplings = trial['couplings']['lengths']

plot = plotting.make_line_data(
    x=time,
    y=[x['value'] for x in couplings],
    y_unc=[x['uncertainty'] for x in couplings],
)

cd.display.plotly(
    data=plot['data'],
    layout=plotting.create_layout(
        title='Coupling Lengths',
        x_label='Cycle (#)',
        y_label='Coupling Length (m)'
    )
)

