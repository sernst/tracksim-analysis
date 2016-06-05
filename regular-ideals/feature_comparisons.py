import plotly.graph_objs as go
import cauldron as cd
from cauldron import plotting

df = cd.shared.couplings_df
df = df[
    (df.duty_cycle < 0.75) &
    (df.collection == 'ideal') &
    (df.gait_number == 1)
]

def comparison_plot(x_name, y_name, color_name, layout):
    traces = []
    for entry in df[color_name].unique():
        sub_df = df[df[color_name] == entry]
        traces.append(go.Scatter(
            x=sub_df[x_name],
            y=sub_df[y_name],
            text=sub_df.uid,
            mode='markers',
            marker={
                'size': 10,
                'color': plotting.get_color(len(traces), 0.75)
            },
            name='{} == {}'.format(color_name, entry)
        ))

    cd.display.plotly(data=traces, layout=layout)

comparison_plot(
    x_name='raw_median',
    y_name='raw_mad',
    color_name='print_interval',
    layout=plotting.create_layout(
        title='Median vs MAD',
        x_label='Median (m)',
        y_label='MAD (m)'
    )
)

comparison_plot(
    x_name='raw_median',
    y_name='raw_swing',
    color_name='print_interval',
    layout=plotting.create_layout(
        title='Median vs Swing',
        x_label='Median (m)',
        y_label='Swing (%)'
    )
)
