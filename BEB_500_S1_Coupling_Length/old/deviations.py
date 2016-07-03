import cauldron as cd
from cauldron import plotting
from plotly import graph_objs as go


def plot_deviations(
        df_row,
        trial,
        deviations,
        threshold: float = 1e6,
        title: str = None,
        y_label: str = None
):
    """
    :param df_row:
    :param trial:
    :param deviations:
    :param threshold:
    :param title:
    :param y_label:
    :return:
    """

    data = trial['couplings']['lengths']
    times = [v['time'] for v in data]

    segments = []

    for time, dev in zip(times, deviations):
        current = segments[-1] if segments else None
        significant = bool(dev > threshold)

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
            title='{} {}'.format(
                trial['short_id'],
                title if title else 'Deviations'
            ),
            x_label='Cycle (#)',
            y_label=y_label if y_label else 'Deviations'
        )
    )

cd.shared.plot_deviations = plot_deviations

cd.display.header('Coupling Length Median Deviations', 2)
cd.display.markdown(
    """
    What we need now is to find any significant deviations in coupling
    length values, if they exist, within each trial. To do that we calculate
    the deviation between the median coupling length for the sample,
    $$C@!L_{median}$$, and the individual coupling length samples, $$C@!L_i$$,
    within in a simulation as:

    $$$
        @Delta_i =
            @frac{ @left| C@!L_{median} - C@!L_i @right| }
                 {@sigma_i}
    $$$

    where $$@sigma_i$$ is the uncertainty for the $$i$$th coupling length.
    Applying the standard 95% significance threshold, any value in excess of
    2.0 represents a statistically significant deviation in coupling length
    from the median value.

    The following show these coupling length median deviations for the same
    simulation trials considered above. The dark grey areas of these plots
    are regions where the coupling length samples did not deviate significantly,
    and the red areas are regions where significant deviations occurred.
    """
)

df = cd.shared.df
df = df[df.gait_id == cd.shared.GAIT_ID].sort_values(by='order')

cd.shared.per_trial(
    df,
    plot_deviations,
    _deviations=cd.shared.deviations,
    threshold=2.1,
    title='Coupling Length Median Deviations',
    y_label='Median Deviation'
)
