import typing

from _Gauge_Quantization.windowing import support
from _Gauge_Quantization.windowing.support import Comparison
from _Gauge_Quantization.windowing.support import IndexedQuantity
from _Gauge_Quantization.windowing.support import Segment


def get_segment(
        all_quantities: typing.List[IndexedQuantity],
        starting_index: int,
        weighted: bool
) -> Segment:
    """ """

    group = [all_quantities[starting_index]]
    comparison = Comparison(median=group[0].quantity, deviation=0)

    for indexed_value in all_quantities[(starting_index + 1):]:
        comparison = support.compare(group, indexed_value, weighted)
        if comparison.deviation > 2:
            break

        group.append(indexed_value)

    end_index = starting_index + len(group)
    return Segment(
        start_index=starting_index,
        stop_index=end_index - 1,
        end_index=end_index,
        quantities=group,
        median=comparison.median
    )


def compute(
        values: list,
        uncertainties: list,
        weighted: bool = True
) -> typing.List[Segment]:
    """ """

    quantities = support.to_quantities(values, uncertainties)
    segments = [get_segment(quantities, 0, weighted=weighted)]

    while segments[-1].end_index < len(quantities):
        start_index = segments[-1].end_index
        segments.append(get_segment(quantities, start_index, weighted))

    return segments
