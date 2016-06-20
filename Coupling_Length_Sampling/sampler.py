import cauldron as cd
import measurement_stats as mstats
from cauldron import plotting

def get_trial(trial_id):
    """

    :param trial_id:
    :return:
    """

    for trial in cd.shared.trials:
        if trial['id'] == trial_id:
            return trial

cd.shared.get_trial = get_trial


def sample(trial):
    """

    :param trial:
    :return:
    """

    out = []
    for index, time in enumerate(trial['times']['cycles']):
        test_time = 2 * time - int(2 * time)
        if mstats.value.equivalent(test_time, 0, 0.001):
            out.append(dict(
                time=time,
                coupling_length=trial['couplings']['lengths'][index]
            ))

    return out

cd.shared.sample = sample


def plot_couplings(*args, **kwargs):
    """

    :param kwargs:
    :param args:
    :return:
    """

    title = kwargs.get('title', 'Coupling Lengths')

    traces = []
    for entry in args:
        trial = entry['trial']
        times = entry.get('times', trial['times']['cycles'])
        lengths = entry.get('lengths', trial['couplings']['lengths'])
        index = entry['index'] if 'index' in entry else trial['group_index']

        if 'color' in entry:
            color = entry['color']
        elif index is None:
            color = plotting.get_gray_color(100, 0.8)
        else:
            color = plotting.get_color(index, 0.8)

        if 'fill_color' in entry:
            fill_color = entry['fill_color']
        elif index is None:
            fill_color = plotting.get_gray_color(100, 0.1)
        else:
            fill_color = plotting.get_color(index, 0.1)

        plot = plotting.make_line_data(
            x=times,
            y=[v['value'] for v in lengths],
            y_unc=[v['uncertainty'] for v in lengths],
            color=color,
            fill_color=fill_color,
            name=entry.get('name', trial['id'])
        )
        traces += plot['data']

    layout = dict(
        showlegend = len(traces) > 0
    )

    cd.display.plotly(
        data=traces,
        layout=plotting.create_layout(
            layout,
            title=title,
            x_label='Cycle (#)',
            y_label='Coupling Length (m)'
        )
    )

cd.shared.plot_couplings = plot_couplings

