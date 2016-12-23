import cauldron as cd
import pandas as pd

from _measurement_uncertainty import trackways

tracks_df = cd.shared.tracks_df


def compute_spreads(trackway_df: pd.DataFrame) -> dict:
    """

    :param trackway_df:
    :return:
    """

    width_spread = int(round(100.0 * float(
        trackway_df['dw_relative'].max() -
        trackway_df['dw_relative'].min()
    )))

    length_spread = int(round(100.0 * float(
        trackway_df['dl_relative'].max() -
        trackway_df['dl_relative'].min()
    )))

    return dict(
        width_spread=width_spread,
        length_spread=length_spread,
        max_spread=max(width_spread, length_spread)
    )


def create_trackway_row(
        trackway_name: str,
        trackway_df: pd.DataFrame
) -> dict:
    """

    :param trackway_name:
    :param trackway_df:
    :return:
    """

    return dict(
        trackway=trackway_name,
        track_count=len(trackway_df),
        **compute_spreads(trackway_df)
    )

trackways_df = pd.DataFrame(
    list(trackways.for_each(create_trackway_row, tracks_df).values())
)

cd.display.markdown(
    """
    ## Spreads per Trackway

    We then use the loaded data to calculate width, length and maximum spreads
    using the equations defined above. The resulting per-trackway spread data
    is:
    """
)

cd.display.table(trackways_df, 0.5)

cd.shared.trackways_df = trackways_df
