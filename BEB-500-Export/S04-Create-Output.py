import cauldron as cd
import pandas as pd
from collections import namedtuple

df_tracks = cd.shared.df_tracks  # type: pd.DataFrame
csv_columns = cd.shared.csv_columns  # type: list


def create_output():
    df = (
        df_tracks[['site', 'level', 'sector', 'uid']]
        .rename(columns={
            'site': csv_columns[1].name,
            'level': csv_columns[2].name,
            'sector': csv_columns[4].name,
        })
    )

    df[csv_columns[0].name] = list(range(1, len(df) + 1))

    df[csv_columns[3].name] = (
        df_tracks['trackwayType']
        .str.cat(df_tracks['trackwayNumber'])
    )

    fills = [column for column in csv_columns if column.fill is not None]
    for column in fills:
        df[column.name] = column.fill

    return df


df_out = create_output()

cd.display.header('Initially Populated Output')
cd.display.table(df_out.head(100), 0.3)

cd.shared.df_out = df_out
