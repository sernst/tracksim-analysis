import cauldron as cd
from cauldron import plotting
import numpy as np
import measurement_stats as mstats
from measurement_stats import distributions as mdist
import plotly.graph_objs as go


def calculate_median(values, uncertainties, color_index=0, plot_name=None):
    """

    :param values:
    :param uncertainties:
    :return:
    """

    try:
        values = values.values
    except:
        pass

    try:
        uncertainties = uncertainties.values
    except:
        pass

    measurements = [
        (val, unc) for val, unc in zip(values, uncertainties)
        if not np.isnan(val) and not np.isnan(unc)
    ]

    values, uncertainties = zip(*measurements)
    measurements = mstats.values.join(values, uncertainties)

    dist = mstats.create_distribution(measurements)
    pop = mdist.population(dist)

    median = mstats.ValueUncertainty(
        mdist.percentile(pop),
        mdist.weighted_median_average_deviation(pop)
    )

    x = mdist.adaptive_range(dist, 4)
    y = dist.probabilities_at(x)

    trace = go.Scatter(
        x=x,
        y=y,
        name=plot_name,
        fill='tozeroy',
        mode='lines',
        line=dict(
            color=plotting.get_color(color_index)
        )
    )

    return dict(
        median=median,
        trace=trace
    )

cd.shared.calculate_median = calculate_median
