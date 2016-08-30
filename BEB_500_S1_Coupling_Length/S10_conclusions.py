import cauldron as cd

df = cd.shared.df
df = df[df['fitness'] > 0.55]

cd.display.header('Highest Fitness Trials', 2)
cd.display.markdown(
    """
    The following are the coupling length plots for the simulation trials
    with the highest fitness values
    """
)
cd.shared.per_trial(df, cd.shared.plot_couplings)
