import math

import cauldron as cd
from cauldron import plotting
import pandas as pd
from plotly import graph_objs as go

df = cd.shared.df  # type: pd.DataFrame

rmsd_normalized = df.rmsd - df.rmsd.min()
rmsd_normalized = rmsd_normalized / rmsd_normalized.max()
df['rmsd_fitness'] = rmsd_normalized

swing_dev_normalized = df.swing_deviation - df.swing_deviation.min()
swing_dev_normalized = swing_dev_normalized / swing_dev_normalized.max()
df['swing_deviation_fitness'] = swing_dev_normalized

cd.display.header('Solution Fitness')

cd.display.markdown(
    """
    Now that we have our to fitness parameters,
    $$@Delta_{RMSD}$$ and
    $$@Delta_{swing}, we combine them
    by plotting each trial on a scatter plot with the parameters as the
    values for each axis. To weight the fitness parameters equally, the values
    for all of the trials have been rescaled to unit range [0, 1].
    """
)

cd.display.plotly(
    data=cd.shared.create_scatter(
        data_frame=cd.shared.df,
        value_column='rmsd_fitness',
        x_column='swing_deviation_fitness'
    ),
    layout=plotting.create_layout(
        {'hovermode': 'closest'},
        title='Solution Fitness',
        x_label='Swing Deviation',
        y_label='RMSD'
    )
)

fitness_values = []


def calculate_fitness(df_row, trial):
    """

    :param df_row:
    :param trial:
    :return:
    """

    x = df_row.swing_deviation_fitness
    y = df_row.rmsd_fitness

    fitness_values.append(math.sqrt(x ** 2 + y ** 2))

cd.shared.per_trial(df, calculate_fitness)

fit_min = min(fitness_values)
fit_max = max(fitness_values)

fitness_values = [
    100 * (1 - (v - fit_min) / fit_max)
    for v in fitness_values
]


cd.display.markdown(
    """
    The closer a particular trial is to origin, the better the solution is
    given our choice of fitness parameters. The Euclidean distance from the
    origin serves as an unbiased indicator of solution quality, and so the
    overall solution fitness is,

    $$$
        fitness = @sqrt{@Delta_{RMSD}^2 + @Delta_{swing}^2}
    $$$

    which is rescaled within the results of the trials to a range of [0,1],
    where one is the best and zero the poorest quality-of-fit.
    """
)

cd.display.plotly(
    data=go.Bar(
        y=fitness_values,
        text=df.short_id,
        marker=dict(
            color=df.color
        )
    ),
    layout=plotting.create_layout(
        title='Solution Fitness',
        x_label='Trial Index (#)',
        y_label='Fitness (%)'
    )
)
