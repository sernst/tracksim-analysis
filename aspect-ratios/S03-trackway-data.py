import cauldron as cd
import pandas as pd
import measurement_stats as mstats
from measurement_stats import distributions as mdist

tracks_df = cd.shared.tracks_df

trackway_data = []


def calculate_median_value(values):
    if not values or not len(values):
        return dict(
            values=[],
            dist=None,
            pop=None,
            median=mstats.ValueUncertainty(0, 0.0001)
        )

    dist = mstats.create_distribution(values)
    pop = mdist.population(dist)
    median = mstats.ValueUncertainty(
        mdist.percentile(pop),
        mdist.weighted_median_average_deviation(pop)
    )
    return dict(
        values=values,
        dist=dist,
        pop=pop,
        median=median
    )
cd.shared.calculate_median_value = calculate_median_value


for trackway_name in tracks_df['trackway'].unique():

    df_slice = tracks_df[tracks_df['trackway'] == trackway_name]

    left_pes_count = len(
        [x for x in df_slice['lp_name'].fillna('').values if x]
    )
    right_pes_count = len(
        [x for x in df_slice['rp_name'].fillna('').values if x]
    )
    left_manus_count = len(
        [x for x in df_slice['lm_name'].fillna('').values if x]
    )
    right_manus_count = len(
        [x for x in df_slice['rm_name'].fillna('').values if x]
    )

    pes_widths = calculate_median_value(
        cd.shared.to_measurements(df_slice, ['lp', 'rp'], 'w')
    )
    pes_lengths = calculate_median_value(
        cd.shared.to_measurements(df_slice, ['lp', 'rp'], 'l')
    )
    pes_aspects = calculate_median_value(
        [l / w for l, w in zip(pes_lengths['values'], pes_widths['values'])]
    )

    manus_widths = calculate_median_value(
        cd.shared.to_measurements(df_slice, ['lm', 'rm'], 'w')
    )
    manus_lengths = calculate_median_value(
        cd.shared.to_measurements(df_slice, ['lm', 'rm'], 'l')
    )
    manus_aspects = calculate_median_value(
        [l / w for l, w in zip(manus_lengths['values'], manus_widths['values'])]
    )

    parts = trackway_name.split('-')
    trackway_data.append(dict(
        lp_count=left_pes_count,
        rp_count=right_pes_count,
        lm_count=left_manus_count,
        rm_count=right_manus_count,
        pes_w=pes_widths['median'].value,
        pes_dw=pes_widths['median'].uncertainty,
        pes_l=pes_lengths['median'].value,
        pes_dl=pes_lengths['median'].uncertainty,
        pes_aspect=pes_aspects['median'].value,
        pes_daspect=pes_aspects['median'].uncertainty,
        manus_w=manus_widths['median'].value,
        manus_dw=manus_widths['median'].uncertainty,
        manus_l=manus_lengths['median'].value,
        manus_dl=manus_lengths['median'].uncertainty,
        manus_aspect=manus_aspects['median'].value,
        manus_daspect=manus_aspects['median'].uncertainty,
        name=trackway_name,
        site=parts[0],
        level=parts[1],
        year=parts[2],
        sector='-'.join(parts[3:-2]),
        number=parts[-1]
    ))

cd.shared.trackway_df = pd.DataFrame(trackway_data)
cd.display.table(cd.shared.trackway_df)
