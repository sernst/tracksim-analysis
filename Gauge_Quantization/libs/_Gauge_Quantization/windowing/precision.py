import functools
import typing

from _Gauge_Quantization.windowing import support
from _Gauge_Quantization.windowing.support import Comparison
from _Gauge_Quantization.windowing.support import IndexedQuantity
from _Gauge_Quantization.windowing.support import Segment


def find_max_precision(
        quantities: typing.List[IndexedQuantity]
) -> typing.Union[IndexedQuantity, None]:
    """
    Returns the value from the values list that has the highest precision, i.e.
    the lowest uncertainty value within the list. If there is a tie among the
    highest precision, the value that appears firs in the list will be returned
    """

    quantities_clean = list(filter(
        lambda v: (v is not None),
        quantities
    ))

    if len(quantities_clean) < 1:
        return None

    if len(quantities_clean) < 2:
        return quantities_clean[0]

    def reducer(best: IndexedQuantity, current: IndexedQuantity):
        replace = (current.quantity.uncertainty < best.quantity.uncertainty)
        return current if replace else best

    return functools.reduce(
        reducer,
        quantities_clean[1:],
        quantities_clean[0]
    )


def is_available(
        quantity: IndexedQuantity,
        segments: typing.List[Segment]
) -> bool:
    """
    Determines whether or not a given measurement is available to be added to
    a segment. The value will be False if the measurement is already included
    in another segment.
    """

    if quantity is None:
        return False

    for segment in segments:
        if quantity in segment.quantities:
            return False
    return True


def get_next_neighbor(
        first_quantity: IndexedQuantity,
        last_quantity: IndexedQuantity,
        all_quantities: typing.List[IndexedQuantity],
        segments: typing.List[Segment]
) -> typing.Union[IndexedQuantity, None]:
    """ """

    if first_quantity is not None:
        index = all_quantities.index(first_quantity)
        before = all_quantities[index - 1] if index > 0 else None
    else:
        before = None

    if last_quantity is not None:
        index = all_quantities.index(last_quantity)
        last_index = len(all_quantities) - 1
        after = all_quantities[index + 1] if index < last_index else None
    else:
        after = None

    return find_max_precision([
        before if is_available(before, segments) else None,
        after if is_available(after, segments) else None
    ])


def get_segment(
        all_quantities: typing.List[IndexedQuantity],
        segments: typing.List[Segment]
) -> typing.Union[Segment, None]:
    """

    :param all_quantities:
    :param segments:
    :return:
    """

    available = [v for v in all_quantities if is_available(v, segments)]
    if not available:
        return None

    group = [find_max_precision(available)]
    comparison = Comparison(median=available[0].quantity, deviation=0)

    for i in range(len(all_quantities)):
        neighbor = get_next_neighbor(
            first_quantity=group[0],
            last_quantity=group[-1],
            all_quantities=all_quantities,
            segments=segments
        )

        if neighbor is None:
            # Breaks the for loop once there is no quantity neighboring the
            # segment that is available for comparison. Either the segment
            # has reached its maximum allowed bounds, or the comparison on
            # either end has yielded a significant deviation.
            break

        group_clean = [quantity for quantity in group if quantity is not None]
        comparison = support.compare(group_clean, neighbor)
        addition = None if comparison.deviation > 2 else neighbor

        neighbor_index = all_quantities.index(neighbor)
        first_index = all_quantities.index(group_clean[0])
        is_before = (neighbor_index < first_index)

        if is_before:
            group.insert(0, addition)
        else:
            group.append(addition)

    quantities_clean = [quantity for quantity in group if quantity is not None]
    return Segment(
        start_index=all_quantities.index(quantities_clean[0]),
        stop_index=all_quantities.index(quantities_clean[-1]),
        end_index=all_quantities.index(quantities_clean[-1]) + 1,
        quantities=quantities_clean,
        median=comparison.median
    )


def compute(values: list, uncertainties: list) -> typing.List[Segment]:
    """ """

    all_quantities = support.to_quantities(values, uncertainties)
    segments = []

    for i in range(len(all_quantities)):
        segment = get_segment(all_quantities, segments)
        if segment is None:
            break

        segments.append(segment)

    return segments
