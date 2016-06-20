import cauldron as cd
from cauldron import plotting

for trial in cd.shared.trials:
    samples = cd.shared.sample(trial)

    cd.shared.plot_couplings(
        dict(
            name='unsampled',
            trial=trial,
            color=plotting.get_gray_color(100, 0.25),
            fill_color=plotting.get_gray_color(100, 0.05)
        ),
        dict(
            name='sampled',
            trial=trial,
            times=[s['time'] for s in samples],
            lengths=[s['coupling_length'] for s in samples]
        ),
        title='{} Coupling Lengths'.format(trial['id'])
    )
