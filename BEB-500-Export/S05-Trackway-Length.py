import cauldron as cd
import pandas as pd
from bokeh.plotting import Figure

df_tracks = cd.shared.df_tracks  # type: pd.DataFrame
df_trackways = cd.shared.df_trackways  # type: pd.DataFrame
df_out = cd.shared.df_out  # type: pd.DataFrame
csv_columns = cd.shared.csv_columns  # type: list


def to_trackway_lengths(row: pd.Series) -> dict:
    trackway_index = row['trackwayIndex']
    trackway = df_trackways.query('index == {}'.format(trackway_index)).iloc[0]

    return {
        'uid': row['uid'],
        csv_columns[8].name: 0.01 * round(100 * trackway['curveLength'])
    }

df = pd.DataFrame([to_trackway_lengths(r) for _, r in df_tracks.iterrows()])
df_out = df_out.drop([csv_columns[8].name], axis=1, errors='ignore')
df_out = pd.merge(left=df_out, right=df, how='inner', on='uid')

cd.display.markdown(
    """
    # Trackway Length

    Trackway length was calculated in Cadence using the curve projection
    algorithms and stored in the analysis.vdb trackways table. The length of a
    trackway was determined by trackway index lookup from each track entry.

    To validate that the trackway lengths were correctly applied on each
    track within a trackway, the values are plotted as a scatter plot for each
    trackway where the tracks are indexed from beginning to end by a
    monotonically increasing integer value. We can visually confirm that the
    values were properly assigned by noting that each trackway is a constant
    line from first to last track.
    """
)

figure = Figure(
    title='Trackway Length per Track',
    x_axis_label='Track Index (#)',
    y_axis_label='Trackway Length'
)


def plot_trackway_lengths(trackway: str):
    tracks = df_out.query('trackway == "{}"'.format(trackway))
    figure.line(list(range(len(tracks))), tracks[csv_columns[8].name])

[plot_trackway_lengths(name) for name in df_out['trackway'].unique()]

cd.display.bokeh(figure)

cd.shared.df_out = df_out
