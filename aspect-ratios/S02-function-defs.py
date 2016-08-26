import cauldron as cd
import measurement_stats as mstats
import numpy as np


def to_measurements(df, limb_ids, property):
    """
    Converts a limb_id value and uncertainty properties to a list of
    measurements

    :param df:
    :param limb_ids:
    :param property:
    :return:
    """

    value_column_names = ['{}_{}'.format(x, property) for x in limb_ids]
    unc_column_names = ['{}_d{}'.format(x, property) for x in limb_ids]

    def is_valid(x):
        if isinstance(x, str):
            return len(x) > 0
        return not np.isnan(x)

    values = []
    for name in value_column_names:
        values += df[name].tolist()
    values = [x for x in values if is_valid(x)]

    uncertainties = []
    for name in unc_column_names:
        uncertainties += df[name].tolist()
        uncertainties = [x for x in uncertainties if is_valid(x)]

    return mstats.values.join(values, uncertainties)

cd.shared.to_measurements = to_measurements

