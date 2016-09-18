import math
import functools

import cauldron as cd
import measurement_stats as mstats
import pandas as pd
from cauldron import plotting
from plotly import graph_objs as go

df = cd.shared.df  # type: pd.DataFrame

swing_normalized = df.swing / df.swing.max()
df['swing_fitness'] = swing_normalized

persistence_normalized = df.persistence / df.persistence.max()
df['persistence_fitness'] = persistence_normalized

cd.display.header('Solution Fitness')

cd.display.markdown(
    """
    Now that we have our two fitness parameters
    $$@Delta_{swing}$$ and
    $$@Delta_{PRSS}$$, we combine them
    by plotting each trial on a scatter plot with the parameters as the
    values for each axis. To weight the fitness parameters equally, the values
    for all of the trials are rescaled to a maximum of 1.
    """
)

traces = []
for gait_id in df.gait_id.unique():
    df_slice = df[df.gait_id == gait_id]
    traces.append(go.Scatter(
        x=df_slice.persistence_fitness,
        y=df_slice.swing_fitness,
        mode='markers',
        marker={
            'size': 8,
            'color': df_slice.iloc[0].color
        },
        name=gait_id,
        text=df_slice.short_id
    ))

cd.display.plotly(
    data=traces,
    layout=plotting.create_layout(
        {'hovermode': 'closest'},
        title='Fitness Parameters',
        x_label='PRSS Fitness',
        y_label='Swing Fitness'
    )
)


fitness_values = []
results_df = []


def calculate_fitness(df_row, trial):
    """

    :param df_row:
    :param trial:
    :return:
    """

    swing = mstats.value.round_to_order(df_row.swing_fitness, -2)
    prss = mstats.value.round_to_order(df_row.persistence_fitness, -2)

    fitness = math.sqrt(swing ** 2 + prss ** 2) / math.sqrt(2)
    fitness_values.append(fitness)

cd.shared.per_trial(df, calculate_fitness)

worst = max(fitness_values)
fitness_values = [worst - v for v in fitness_values]

df['fitness'] = fitness_values

cd.display.markdown(
    """
    The closer a particular trial is to origin of this fitness parameter space,
    the more efficacious of a solution the trial is for the trackway. Computing
    the Euclidean distance for each point creates the final fitness parameter
    ranking for the trials,

    $$$
        fitness = @sqrt{
            @Delta_{swing}^2 +
            @Delta_{PRSS}^2
        }
    $$$

    And finally, to more clearly present the quality-of-fitness the fitness
    for each trial is subtracted from the poorest fitness to yield:
    """
)

cd.display.plotly(
    cd.shared.create_stem(df, fitness_values),
    layout=plotting.create_layout(
        title='Solution Fitness',
        x_label='Coupling Length (m)',
        y_label='Fitness'
    )
)


