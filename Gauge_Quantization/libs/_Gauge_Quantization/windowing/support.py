import typing
import math
import measurement_stats as mstats
import measurement_stats.distributions as mdist
from collections import namedtuple
import numpy as np

import pandas as pd
import cauldron

IndexedQuantity = namedtuple('IndexedValue_NT', ['index', 'quantity'])

Comparison = namedtuple('Comparison_NT', ['median', 'deviation'])

Segment = namedtuple('Segment_NT', [
    'start_index',
    'stop_index',
    'end_index',
    'quantities',
    'median'
])


def to_quantities(
        values: list,
        uncertainties: list
) -> typing.List[IndexedQuantity]:
    """
    Converts two lists of values and uncertainties into a single list of
    indexed quantities.
    """

    return [
        IndexedQuantity(i, v)
        for i, v in enumerate(mstats.values.join(values, uncertainties))
    ]


def get_weighted_median(quantities) -> mstats.ValueUncertainty:
    dist = mstats.create_distribution(quantities)
    pop = mdist.population(dist)
    return mstats.ValueUncertainty(
        mdist.percentile(pop, 0.5),
        max(0.00001, mdist.weighted_median_average_deviation(pop))
    )


def get_unweighted_median(quantities) -> mstats.ValueUncertainty:
    values = [q.value for q in quantities]
    median_value = np.median(values)
    median_absolute_deviation = np.median([
        abs(value - median_value)
        for value in values
    ])

    return mstats.ValueUncertainty(
        median_value,
        max(0.00001, median_absolute_deviation)
    )


def compare(
        group: typing.List[IndexedQuantity],
        other: IndexedQuantity,
        weighted: bool = True
) -> Comparison:
    """
    Compares a group of one or more quantities against another quantity and
    returns the comparison result of the deviation between the group and the
    other value.

    :param group:
        The group of one or more indexed quantities to use as the source of
        comparison
    :param other:
        The quantity to be compared against the group
    :param weighted:
        Whether or not the median value for the group should be calculated
        using uncertainty weighting or not
    :return:
        The result of the comparison between the group of quantities and the
        other quantity
    """

    cauldron.step.breathe()

    quantities = [v.quantity for v in group]

    median = (
        get_weighted_median(quantities)
        if weighted else
        get_unweighted_median(quantities)
    )

    delta = abs(median.value - other.quantity.value)
    error = math.sqrt(
        median.uncertainty ** 2 +
        other.quantity.uncertainty ** 2
    )

    cauldron.step.breathe()

    return Comparison(median=median, deviation=delta / error)


def get_segment_bounds(
        quantities: typing.List[IndexedQuantity],
        tracks: pd.DataFrame
) -> typing.Tuple[float, float]:

    def get_midpoint_between(before_index: int, after_index: int) -> float:
        positions = tracks['curvePosition'].values

        if before_index < 0:
            return positions[0] - 0.05
        elif after_index >= (len(positions) - 1):
            return positions[-1] + 0.05

        return (positions[before_index] + positions[after_index]) / 2

    if not quantities:
        return 0, 0

    first_index = quantities[0].index  # type: int
    last_index = quantities[-1].index  # type: int
    return (
        get_midpoint_between(first_index - 1, first_index),
        get_midpoint_between(last_index, last_index + 1)
    )
