import cauldron as cd
from cauldron import plotting
import measurement_stats as mstats


def plot_smoothed(size):

    trial = cd.shared.trial
    steps_per_cycle = trial['settings']['steps_per_cycle']
    time = trial['times']['cycles']
    couplings = trial['couplings']['lengths']

    couplings = mstats.values.from_serialized(couplings)
    couplings = mstats.values.windowed_smooth(couplings, size, 256)
    values, uncertainties = mstats.values.unzip(couplings)

    plot = plotting.make_line_data(
        x=time,
        y=values,
        y_unc=uncertainties,
    )

    coverage = 100 * (2 * size + 1) / steps_per_cycle

    cd.display.plotly(
        data=plot['data'],
        layout=plotting.create_layout(
            title='Smoothed Coupling Lengths (Cycle Coverage {}%)'.format(
                coverage
            ),
            x_label='Cycle (#)',
            y_label='Coupling Length (m)'
        )
    )

cd.shared.plot_smoothed = plot_smoothed

plot_smoothed(1)

