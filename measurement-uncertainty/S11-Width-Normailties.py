import cauldron as cd
import pandas as pd
import measurement_stats as mstats


from _measurement_uncertainty import trackways

pes_df = cd.shared.tracks_df.query('is_pes == True')


def to_distribution(key: str, trackway_df: pd.DataFrame) -> mstats.Distribution:
    """
    Converts a trackway data frame to a measurement distribution for the
    specified key

    :param key:
        Lookup key within the trackway data frame. Assumes that key exists
        as a column in the data frame and that the uncertainties for those
        values are stored in a column named d{key}.
    :param trackway_df:
    :return:
        A measurement distribution for the selected measurements
    """

    return mstats.create_distribution(
        trackway_df[key].tolist(),
        trackway_df['d{}'.format(key)].tolist()
    )


def compute_normality_unweighted(
        key: str,
        trackway_df: pd.DataFrame
) -> mstats.ValueUncertainty:
    dist = to_distribution(key, trackway_df)
    mean = mstats.mean.unweighted(*dist.measurements)
    comparison = mstats.create_distribution([mean])
    return mstats.distributions.overlap2(dist, comparison)


def compute_normality_weighted(
        key: str,
        trackway_df: pd.DataFrame
) -> mstats.ValueUncertainty:
    dist = to_distribution(key, trackway_df)
    mean = mstats.mean.weighted(*dist.measurements)
    comparison = mstats.create_distribution([mean])
    return 1.0 - mstats.distributions.overlap2(dist, comparison)


def get_normalities(
        trackway_name: str,
        trackway_df: pd.DataFrame,
        progress: float
) -> dict:
    if len(trackway_df) < 10:
        return None

    cd.display.status(section_message=trackway_name)

    width_norm_unweighted = compute_normality_unweighted('w', trackway_df)
    cd.display.status(section_progress=0.25)
    width_norm_weighted = compute_normality_weighted('w', trackway_df)
    cd.display.status(section_progress=0.5)
    length_norm_unweighted = compute_normality_unweighted('l', trackway_df)
    cd.display.status(section_progress=0.75)
    length_norm_weighted = compute_normality_weighted('l', trackway_df)

    cd.display.status(
        '{}% complete'.format(int(100 * progress)),
        progress=progress,
        section_progress=1
    )

    return dict(
        trackway_name=trackway_name,
        width_norm_unweighted=width_norm_unweighted.value,
        width_norm_weighted=width_norm_weighted.value,
        width_norm_delta=(width_norm_weighted - width_norm_unweighted).value,
        length_norm_unweighted=width_norm_unweighted.value,
        length_norm_weighted=width_norm_weighted.value,
        length_norm_delta=(length_norm_weighted - length_norm_unweighted).value,
    )

trackway_names_slice = pes_df['trackway'].unique()[:5]

tracks_df = pes_df[pes_df['trackway'].isin(trackway_names_slice)]

normalities_df = pd.DataFrame(list(filter(
    lambda data: (data is not None),
    trackways.for_each(get_normalities, pes_df).values()
)))

cd.display.table(normalities_df)
cd.shared.normalities_df = normalities_df
