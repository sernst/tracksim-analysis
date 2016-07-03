import cauldron as cd
from cauldron import plotting
from plotly import graph_objs as go

df = cd.shared.df_remaining

cd.display.header('Median Deviation Indicator')
cd.display.markdown(
    """
    We now return to the median deviations parameter discussed earlier. In
    the previous formulation, the median deviations was used to find
    statistically significant deviations...

    $$$

    $$$

    """
)

cd.display.plotly(
    data=go.Bar(
        y=[max(cd.shared.scaled_deviations[tid]) for tid in df.id],
        text=df.short_id,
        marker=dict(
            color=df.color
        )
    ),
    layout=plotting.create_layout(
        title='Fractional Median Deviations',
        x_label='Trial Index (#)',
        y_label='Fractional Deviation'
    )
)


def compute_deviations_per_cycle():
    """

    :return:
    """

    out = [sum(cd.shared.deviations[tid]) for tid in df.id]
    for index, tid in enumerate(df.id):
        for trial in cd.shared.trials:
            if trial['id'] == tid:
                break
        start_time = trial['couplings']['lengths'][0]['time']
        end_time = trial['couplings']['lengths'][-1]['time']
        out[index] /= end_time - start_time

    return out


cd.display.plotly(
    data=go.Bar(
        y=compute_deviations_per_cycle(),
        text=df.short_id,
        marker=dict(
            color=df.color
        )
    ),
    layout=plotting.create_layout(
        title='Cycle-Averaged Coupling Length Median Deviations',
        x_label='Trial Index (#)',
        y_label='Value'
    )
)

