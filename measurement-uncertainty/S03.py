import cauldron as cd
import numpy as np
import measurement_stats as mstats
import pandas as pd
import plotly.graph_objs as go

from _measurement_uncertainty import trackways


df_tracks = cd.shared.tracks_df
df_pes = df_tracks[df_tracks['is_pes']]


def calculate_widths(name, df, progress):
    cd.display.status('Calculating Width Values', progress=progress)
    values = mstats.values.join(df['w'].tolist(), df['dw'].tolist())
    dist = mstats.create_distribution(values)

    mean_weighted = mstats.mean.weighted(values)

    return dict(
        trackway=name,
        mean=mstats.mean.unweighted(values).raw,
        mean_weighted=mean_weighted.value,
        mean_weighted_unc=mean_weighted.uncertainty,
        median=np.median(df['w']),
        median_weighted=mstats.distributions.percentile(dist),
        median_weighted_unc=mstats.distributions.weighted_median_average_deviation(dist)
    )


def compute_fractional_deviation(value: pd.Series, actual: pd.Series) -> pd.Series:
    return (value - actual).abs() / actual


def compute_deviation(
        value: pd.Series,
        actual: pd.Series,
        uncertainty: pd.Series
) -> pd.Series:
    return (value - actual).abs() / uncertainty


def add_deviations(data_frame: pd.DataFrame):
    df = data_frame.copy() # type: pd.DataFrame
    cd.display.table(df)

    df['mean_deviation'] = compute_deviation(
        df['mean'],
        df['mean_weighted'],
        df['mean_weighted_unc']
    )
    df['mean_frac_deviation'] = compute_fractional_deviation(
        df['mean'],
        df['mean_weighted']
    )

    df['median_deviation'] = compute_deviation(
        df['median'],
        df['median_weighted'],
        df['median_weighted_unc']
    )
    df['median_frac_deviation'] = compute_fractional_deviation(
        df['median'],
        df['median_weighted']
    )
    return df


trackway_widths = trackways.for_each(calculate_widths, df_pes)
df_pes_widths = add_deviations(pd.DataFrame(list(trackway_widths.values())))

cd.display.plotly(
    go.Histogram(
        x=df_pes_widths['mean_frac_deviation']
    ),
    {}
)

cd.display.plotly(
    go.Histogram(
        x=df_pes_widths['median_frac_deviation']
    ),
    {}
)
