import cauldron as cd
import measurement_stats as mstats
import pandas as pd

df = cd.shared.df  # type: pd.DataFrame
deviations = dict()
scaled_deviations = dict()

relative_uncertainty_min = df.relative_uncertainty.min()


def calculate_deviations(df_row, trial):
    """

    :param df_row:
    :param trial:
    :return:
    """

    median = mstats.ValueUncertainty(**trial['couplings']['value'])
    couplings = mstats.values.from_serialized(
        [cl['value'] for cl in trial['couplings']['lengths']]
    )

    deviations[trial['id']] = [
        abs(cl.value - median.value) / cl.uncertainty
        for cl in couplings
        ]

    relative_uncertainty = df[df.id == trial['id']].relative_uncertainty
    scale = float(relative_uncertainty / relative_uncertainty_min)

    scaled_deviations[trial['id']] = [
        scale * abs(cl.value - median.value) / cl.uncertainty
        for cl in couplings
        ]

cd.shared.per_trial(df, calculate_deviations)
cd.shared.deviations = deviations
cd.shared.scaled_deviations = scaled_deviations
