import cauldron as cd
from cauldron import plotting
import measurement_stats as mstats
from plotly import graph_objs as go


def plot_median_deviations(trial):
    """

    :param trial:
    :return:
    """

    median = mstats.ValueUncertainty(**trial['couplings']['value'])
    data = trial['couplings']['lengths']
    times = [v['time'] for v in data]
    couplings = mstats.values.from_serialized([v['value'] for v in data])

    deviations = [
        abs(cl.value - median.value) / cl.uncertainty
        for cl in couplings
    ]

    segments = []

    for time, dev in zip(times, deviations):
        current = segments[-1] if segments else None
        significant = bool(dev > 2.1)

        if not current or current['significant'] != significant:
            segments.append(dict(
                significant=significant,
                times=[time],
                devs=[dev]
            ))
            if not current or not current['times']:
                continue

            if significant:
                segments[-1]['times'].insert(0, current['times'][-1])
                segments[-1]['devs'].insert(0, current['devs'][-1])
            else:
                current['times'].append(time)
                current['devs'].append(dev)
            continue

        current['times'].append(time)
        current['devs'].append(dev)

    segments.sort(key=lambda x: 1 if x['significant'] else 0)

    traces = []
    for segment in segments:
        sig = segment['significant']

        traces.append(go.Scatter(
            x=segment['times'],
            y=segment['devs'],
            mode='lines+markers',
            line=dict(
                color='#CC3333' if sig else '#333'
            ),
            marker=dict(
                color='#CC3333' if sig else '#333'
            ),
            fill='tozeroy'
        ))

    cd.display.plotly(
        data=traces,
        layout=plotting.create_layout(
            dict(
                showlegend=False
            ),
            title='{} Coupling Length Median Deviations'.format(
                trial['id'].split('_', 1)[0]
            ),
            x_label='Cycle (#)',
            y_label='Fractional Deviation'
        )
    )

cd.shared.plot_median_deviations = plot_median_deviations

df = cd.shared.df
df = df[df.gait_id == cd.shared.GAIT_ID].sort_values(by='coupling_length')

cd.display.header('Coupling Length Median Deviations', 2)
cd.display.markdown(
    """
    What we need now is to determine any significant deviations in coupling
    length values, if they exist, within each trial. To do that we plot the
    fractional deviation between each coupling length sample in a simulation
    and the median coupling length value for the entire simulation. In
    accordance with standard practice, the threshold for a significant
    difference between a median coupling length and a sample is two.

    The plots below show these coupling length median deviation for the same
    simulation trials considered above. The dark grey areas of these plots
    are regions where the coupling length samples did not deviate significantly,
    and the red areas are regions of significant deviation from the median.
    """
)

cd.shared.per_trial(df, plot_median_deviations)
