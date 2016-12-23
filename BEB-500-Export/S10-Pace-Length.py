import cauldron as cd
import pandas as pd
from bokeh.plotting import Figure

df_tracks = cd.shared.df_tracks  # type: pd.DataFrame
df_out = cd.shared.df_out  # type: pd.DataFrame
csv_columns = cd.shared.csv_columns  # type: pd.DataFrame

GUESS_THRESHOLD = 0.2


def create(**kwargs) -> dict:
    pairs = [
        (csv_columns[index].name, None)
        for index in (48, 49, 52, 53, 63, 64, 67, 68)
    ]

    return dict(pairs, **kwargs)


def get_indices(track: pd.Series) -> tuple:
    if track['pes']:
        return (48, 49) if track['left'] else (52, 53)

    return (63, 64) if track['left'] else (67, 68)


def to_pace(track: pd.Series) -> dict:
    out = create(uid=track['uid'])

    if not track['paceLength'] or track['paceLength'] >= 3:
        return out

    indices = get_indices(track)
    is_guess = (0.2 <= (track['paceLengthUnc'] / track['paceLength']))
    index = indices[1] if is_guess else indices[0]
    pace_length = 0.01 * round(100 * track['paceLength'])
    out.update({
        csv_columns[index].name: pace_length,
    })
    return out


df = pd.DataFrame([to_pace(t) for _, t in df_tracks.iterrows()])

for key in create().keys():
    df_out = df_out.drop([key], axis=1, errors='ignore')
df_out = pd.merge(df_out, df, on='uid')

cd.display.markdown(
    """
    # Pace Length

    The curve projection algorithm made it possible for Cadence
    to determine pace lengths algorithmically by using curve indexing
    to create pace pairs. The pace length values are stored in the tracks
    analysis database table and can be exported from there. The only
    complication is the determination of guess versus non-guess column
    assignment, which is done using the uncertainties that were computed for
    each pace length during Cadence analysis.
    """
)

df_plot = pd.DataFrame(dict(
    uid=df_out['uid'],
    pace=(
        df_out[csv_columns[48].name]
        .fillna(df_out[csv_columns[49].name])
        .fillna(df_out[csv_columns[52].name])
        .fillna(df_out[csv_columns[53].name])
        .fillna(df_out[csv_columns[63].name])
        .fillna(df_out[csv_columns[64].name])
        .fillna(df_out[csv_columns[67].name])
        .fillna(df_out[csv_columns[68].name])
    )
))
df_plot = pd.merge(
    df_plot,
    df_tracks[['uid', 'width']],
    on='uid',
    how='left'
).dropna()

figure = Figure(
    title='Pace Length versus Foot Width'
)
figure.scatter(x=df_plot['width'], y=df_plot['pace'])
cd.display.bokeh(figure)

cd.display.markdown(
    """
    There are a few pace length outliers as shown in the plot, but a deeper
    analysis would be needed to resolve them. The large majority of pace values
    look consistent with expectations.
    """
)

cd.shared.df_out = df_out
