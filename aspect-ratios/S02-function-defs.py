import cauldron as cd
from cauldron import plotting
import numpy as np
import measurement_stats as mstats
import plotly.graph_objs as go


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


def process(df):
    """

    :param df:
    :return:
    """

    print('Track Counts:')

    total = 0
    for limb_id in ['lp', 'rp', 'lm', 'rm']:
        data = df['{}_name'.format(limb_id)].fillna('').values
        names = [x for x in data if x]
        total += len(names)
        print('{}:'.format(limb_id.upper()), len(names))
    print('Total:', total)

    widths = cd.shared.to_measurements(df, ['lp', 'rp'], 'w')
    lengths = cd.shared.to_measurements(df, ['lp', 'rp'], 'l')

    aspects = []
    for w, l in zip(widths, lengths):
        aspects.append(l / w)

    dist = mstats.create_distribution(aspects)
    population = mstats.distributions.population(dist)
    median = mstats.distributions.percentile(population)
    mad = mstats.distributions.weighted_median_average_deviation(population)

    median = mstats.ValueUncertainty(median, mad)

    print('\nMedian Pes Aspect Ratio:', median.label)

    x = mstats.distributions.adaptive_range(dist, 5)
    y = dist.probabilities_at(x)

    cd.display.plotly(
        data=go.Scatter(
            x=x,
            y=y,
            mode='lines'
        ),
        layout=plotting.create_layout(
            {},
            title='Weighted Pes Aspect Ratio Distribution',
            x_label='Pes Aspect Ratio (length / width)',
            y_label='Probability (AU)'
        )
    )

    cd.display.plotly(
        data=go.Histogram(
            x=df['lp_w'].values + df['rp_w'].values,
            autobinx=False,
            xbins=dict(
                start=0,
                end=2.0,
                size=0.0125
            )
        ),
        layout=plotting.create_layout(
            {},
            title='Pes Width Distributions',
            x_label='Width (m)',
            y_label='Frequency (#)',
            x_bounds=[0, 2.0]
        )
    )

    cd.display.plotly(
        data=go.Histogram(
            x=df['lp_l'].values + df['rp_l'].values,
            autobinx=False,
            xbins=dict(
                start=0,
                end=2.0,
                size=0.0125
            )
        ),
        layout=plotting.create_layout(
            {},
            title='Pes Length Distributions',
            x_label='Length (m)',
            y_label='Frequency (#)',
            x_bounds=[0, 2.0]
        )
    )

cd.shared.process = process
