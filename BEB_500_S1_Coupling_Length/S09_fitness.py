import math

import cauldron as cd
import measurement_stats as mstats
import pandas as pd
from cauldron import plotting

df = cd.shared.df  # type: pd.DataFrame

swing_normalized = df.swing / df.swing.max()
df['swing_fitness'] = swing_normalized

persistence_normalized = df.persistence / df.persistence.max()
df['persistence_fitness'] = persistence_normalized

cd.display.header('Solution Fitness')

cd.display.markdown(
    """
    Now that we have our to fitness parameters
    $$@Delta_{swing}$$ and
    $$@Delta_{PRSS}$$, we combine them
    by plotting each trial on a scatter plot with the parameters as the
    values for each axis. To weight the fitness parameters equally, the values
    for all of the trials have been rescaled to a maximum of 1.
    """
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

    results_df.append(dict(
        id=df_row.short_id,
        swing=swing,
        prss=prss,
        total=fitness
    ))

cd.shared.per_trial(df, calculate_fitness)

fit_min = min(fitness_values)
fit_max = max(fitness_values)

fitness_values = [round(100 * (1 - min(1.0, v))) for v in fitness_values]

results_df = pd.DataFrame(results_df)
results_df['fitness'] = fitness_values
cd.display.table(results_df)

cd.display.markdown(
    """
    The closer a particular trial is to origin, the better the solution is
    given our choice of fitness parameters. The Euclidean distance from the
    origin serves as an unbiased indicator of solution quality, and so the
    overall solution fitness is,

    $$$
        fitness = @frac
            {
                1 - @sqrt{
                    @Delta_{swing}^2 +
                    @Delta_{PRSS}^2
                }
            }
            { @sqrt{2} }
    $$$

    which is rescaled within the results of the trials to a range of [0,1],
    where one is the best and zero the poorest quality-of-fit.
    """
)

cd.display.plotly(
    cd.shared.create_stem(df, fitness_values),
    layout=plotting.create_layout(
        title='Solution Fitness',
        x_label='Coupling Length (m)',
        y_label='Fitness (%)'
    )
)
