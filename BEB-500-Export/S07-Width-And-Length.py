import cauldron as cd
import pandas as pd
from bokeh.plotting import Figure

df_tracks = cd.shared.df_tracks  # type: pd.DataFrame
df_out = cd.shared.df_out  # type: pd.DataFrame
csv_columns = cd.shared.csv_columns  # type: list

GUESS_THRESHOLD = 0.2


def create(**kwargs) -> dict:
    out = dict([
        (column.name, None)
        for column in (csv_columns[23:27] + csv_columns[33:37])
    ])
    out.update(**kwargs)
    return out


def get_size(
        row: pd.Series,
        label: str,
        match: bool,
        index: int,
        guess_index: int
) -> dict:
    if not match:
        return dict()

    value = row[label]
    uncertainty = row['{}Uncertainty'.format(label)]
    delta = uncertainty / value
    is_guess = (delta >= GUESS_THRESHOLD)

    column = csv_columns[guess_index] if is_guess else csv_columns[index]
    return {column.name: value}


def to_width_length(row: pd.Series) -> dict:
    out = create(uid=row['uid'])
    out.update(get_size(row, 'length', row['pes'], 23, 24))
    out.update(get_size(row, 'width', row['pes'], 25, 26))
    out.update(get_size(row, 'length', not row['pes'], 33, 34))
    out.update(get_size(row, 'width', not row['pes'], 35, 36))
    return out

df = pd.DataFrame([to_width_length(r) for _, r in df_tracks.iterrows()])

for key in create().keys():
    df_out = df_out.drop([key], axis=1, errors='ignore')

df_out = pd.merge(left=df_out, right=df, how='inner', on='uid')
figure = Figure(
    title='Track Lengths and Widths',
    x_axis_label='Track Length (m)',
    y_axis_label='Track Width (m)'
)

figure.scatter(
    df_out[csv_columns[23].name].fillna(df_out[csv_columns[24].name]),
    df_out[csv_columns[25].name].fillna(df_out[csv_columns[26].name]),
    color='blue',
    legend='Pes'
)

figure.scatter(
    df_out[csv_columns[33].name].fillna(df_out[csv_columns[34].name]),
    df_out[csv_columns[35].name].fillna(df_out[csv_columns[36].name]),
    color='red',
    legend='Manus'
)


cd.display.markdown(
    """
    # Track Width and Length

    Track widths and lengths can be used directly from the Cadence database
    values. The catalog separates out width and length values with high amounts
    of relative uncertainty and places their values in separate _guess_
    columns. Cadence database values have associated uncertainties, which are
    used to determine whether or not to place the values in the standard value
    column or the guess column. Any values with relative uncertainties equal
    to or greater than {{ guess_threshold }}% are placed in the _guess_ column.

    The following plot shows the scatter of width and length values for all
    tracks in the database after export.
    """,
    guess_threshold=int(100 * GUESS_THRESHOLD)
)

cd.display.bokeh(figure)

cd.shared.df_out = df_out
