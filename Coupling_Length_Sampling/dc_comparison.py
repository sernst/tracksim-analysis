import pandas as pd
import cauldron as cd

df = cd.shared.df  # type: pd.DataFrame


def plot_cd_comparison(gait_id, spacing):
    """

    :param gait_id:
    :param spacing:
    :return:
    """

    segment = df[
        (df.gait_id == gait_id) &
        (df.spacing == spacing)
    ]

    entries = []
    for index, row in segment.iterrows():
        trial = cd.shared.get_trial(row.id)

        entries.append(dict(
            index=len(entries),
            trial=trial,
            name='DC {}'.format(row.duty_cycle)
        ))

    cd.shared.plot_couplings(
        *entries,
        title='Coupling Length ({}-{})'.format(gait_id, spacing)
    )

plot_cd_comparison('G4', 1)
plot_cd_comparison('G2', 1)
