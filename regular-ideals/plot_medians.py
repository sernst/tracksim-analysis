import cauldron as cd
import plotly.graph_objs as go
from cauldron import plotting

df = cd.shared.couplings_df
df['deviation'] = 100.0 * df['raw_swing'] / df['raw_median']

df = df[
    (df.duty_cycle < 0.75) &
    (df.gait_number == 1)
]
df = df.sort_values(by='gait_id')
df['ordered_index'] = list(range(df.shape[0]))

traces = []

for pi in df['print_interval'].unique():
    sub_df = df[df.print_interval == pi]
    traces.append(go.Bar(
        x=sub_df.ordered_index,
        y=sub_df['deviation'],
        text=sub_df['uid'],
        name='Print Interval {}'.format(pi)
    ))

cd.display.plotly(
    data=traces,
    layout=plotting.create_layout(
        title='Median Coupling Length Swing (Min, Max)',
        x_label='Trial Index (#)',
        y_label='Median Swing (%)'
    )
)

df = cd.shared.couplings_df
df['deviation'] = 100.0 * df['smooth_swing'] / df['raw_median']

df = df[
    (df.duty_cycle < 0.75) &
    (df.gait_number == 1)
]
df = df.sort_values(by='gait_id')
df['ordered_index'] = list(range(df.shape[0]))

traces = []

for pi in df['print_interval'].unique():
    sub_df = df[df.print_interval == pi]
    traces.append(go.Bar(
        x=sub_df.ordered_index,
        y=sub_df['deviation'],
        text=sub_df['uid'],
        name='Print Interval {}'.format(pi)
    ))

cd.display.plotly(
    data=traces,
    layout=plotting.create_layout(
        title='Smoothed Median Coupling Length Swing (Min, Max)',
        x_label='Trial Index (#)',
        y_label='Median Swing (%)'
    )
)

df = cd.shared.couplings_df
df['deviation'] = 100.0 * df['raw_mad'] / df['raw_median']

df = df[
    (df.duty_cycle < 0.75) &
    (df.gait_number == 1)
]
df = df.sort_values(by='gait_id')
df['ordered_index'] = list(range(df.shape[0]))

traces = []

for pi in df['print_interval'].unique():
    sub_df = df[df.print_interval == pi]
    traces.append(go.Bar(
        x=sub_df.ordered_index,
        y=sub_df['deviation'],
        text=sub_df['uid'],
        name='Print Interval {}'.format(pi)
    ))

cd.display.plotly(
    data=traces,
    layout=plotting.create_layout(
        title='Coupling Lengths Median Absolute Deviation (MAD)',
        x_label='Trial Index (#)',
        y_label='MAD (%)'
    )
)

