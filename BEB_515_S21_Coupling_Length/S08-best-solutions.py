import cauldron as cd
from cauldron import plotting
from tracksim.coupling.plotting import band

cd.refresh(band)

df = cd.shared.df.sort_values(by='fitness', ascending=False).head()

cd.display.header('Highest Fitness Trials', 2)
cd.display.markdown(
    """
    The following are the coupling length plots for the simulation trials
    with the highest fitness values
    """
)


def plot(trial):
    plot_data = band.coupling(trial)
    cd.display.plotly(
        data=plot_data['data'],
        layout=plotting.create_layout(
            plot_data['layout'],
            title='{} Coupling Length'.format(trial['short_id']),
            x_label='Cycle (#)',
            y_label='Coupling Length (m)'
        )
    )

ids = df['id'].tolist()

for t in cd.shared.trials:
    if t['id'] in ids:
        plot(t)
