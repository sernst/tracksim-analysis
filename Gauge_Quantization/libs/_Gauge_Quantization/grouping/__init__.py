import typing
import math
from collections import namedtuple
import pandas as pd

import measurement_stats as mstats
from measurement_stats import distributions as mdist
import cauldron

from _Gauge_Quantization.windowing.support import Segment

SegmentList = typing.List[Segment]

SegmentGroup = namedtuple('SegmentGroup_NT', [
    'index',
    'segments',
    'median',
    'normalized_median'
])

SegmentGroupList = typing.List[SegmentGroup]


def get_median(
        quantities: typing.List[mstats.ValueUncertainty]
) -> mstats.ValueUncertainty:
    dist = mstats.create_distribution(quantities)
    pop = mdist.population(dist)
    return mstats.ValueUncertainty(
        mdist.percentile(pop, 0.5),
        max(0.00001, mdist.weighted_median_average_deviation(pop))
    )


def add_to_group(
        segment: Segment,
        groups: SegmentGroupList,
        trackway_data: dict
) -> SegmentGroupList:
    """

    :param segment:
    :param groups:
    :param trackway_data:
    :return:
    """

    deviations = [deviation_between(g, segment) for g in groups]

    if not deviations or min(deviations) > 2:
        return groups + [SegmentGroup(
            index=len(groups),
            segments=[segment],
            median=segment.median,
            normalized_median=segment.median / trackway_data['width_median']
        )]

    group_index = deviations.index(min(deviations))
    group = groups[group_index]

    cauldron.step.breathe()

    dist = mstats.create_distribution([s.median for s in group.segments])
    pop = mdist.population(dist)
    median = mstats.ValueUncertainty(
        mdist.percentile(pop, 0.5),
        max(0.00001, mdist.weighted_median_average_deviation(pop))
    )

    normalized = median / trackway_data['width_median']

    replacement_group = SegmentGroup(
        index=group.index,
        median=median,
        segments=group.segments + [segment],
        normalized_median=normalized
    )

    return (
        groups[:group_index] +
        [replacement_group] +
        groups[(group_index + 1):]
    )


def deviation_between(
        group: SegmentGroup,
        segment: Segment
) -> float:

    delta = abs(segment.median.value - group.median.value)
    error = math.sqrt(
        segment.median.uncertainty ** 2 +
        group.median.uncertainty ** 2
    )

    return delta / max(0.00001, error)


def order_by_precision(segments: SegmentList) -> SegmentList:
    return sorted(segments, key=lambda s: s.median.uncertainty)


def get_trackway_data(tracks: pd.DataFrame):
    width_median = get_median(mstats.values.join(
        tracks['width'].tolist(),
        tracks['widthUncertainty'].tolist()
    ))

    return dict(
        tracks=tracks,
        width_median=width_median,
        length=tracks['curvePosition'].max()
    )


def combine(
        segments: SegmentList,
        tracks: pd.DataFrame
) -> typing.List[SegmentGroup]:
    """

    :param segments:
    :param tracks:
    :return:
    """

    trackway_data = get_trackway_data(tracks)
    ordered = order_by_precision(segments)
    groups = []

    for segment in ordered[1:]:
        groups = add_to_group(segment, groups, trackway_data)
    return groups



