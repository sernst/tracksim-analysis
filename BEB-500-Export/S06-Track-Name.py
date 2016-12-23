import cauldron as cd
import pandas as pd
from bokeh.charts import Bar

df_tracks = cd.shared.df_tracks  # type: pd.DataFrame
df_out = cd.shared.df_out  # type: pd.DataFrame
csv_columns = cd.shared.csv_columns


def to_track_names(row: pd.Series) -> dict:
    name = '{}{}{}'.format(
        'L' if row['left'] else 'R',
        'P' if row['pes'] else 'M',
        row['number']
    )

    return {
        'uid': row['uid'],
        csv_columns[21].name: name
    }


df = pd.DataFrame([to_track_names(r) for _, r in df_tracks.iterrows()])

df_out = df_out.drop([csv_columns[21].name], axis=1, errors='ignore')
df_out = pd.merge(left=df_out, right=df, how='inner', on='uid')


cd.display.markdown(
    """
    # Track Name

    The track_name is assembled from the left, pes and number columns of the
    tracks table. The following are the unique track name values assigned from
    the Cadence database entries.
    """
)

entries = [
    '<div style="width: 60px; padding: 0.25em;">{}</div>'.format(entry)
    for entry in df_out[csv_columns[21].name].unique()
]

cd.display.html('<div style="display: flex; flex-wrap: wrap;">{}</div>'.format(
    ''.join(entries)
))

cd.shared.df_out = df_out
