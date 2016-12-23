import os
import cauldron as cd
import pandas as pd
from sqlalchemy import create_engine
import re

database_directory = os.path.join(
    os.path.expanduser('~'),
    'Dropbox',
    'A16',
    'Notebook-Data',
    'cadence-databases'
)


def renaming_mapper(column_name):
    """

    :param column_name:
    :return:
    """

    if re.compile('^[^a-zA-Z_]+').match(column_name):
        return 'X{}'.format(column_name)
    return column_name


def read_table(table_name, engine):
    """

    :param table_name:
    :param engine:
    :return:
    """

    df = pd.read_sql_table(table_name, engine)
    df.columns = map(renaming_mapper, list(df.columns))
    return df


def keep_column(column_name: str) -> bool:
    if not column_name or column_name.startswith('_'):
        return False

    if column_name in ['snapshot', 'dead']:
        return False

    return True


def purge_columns(df_source: pd.DataFrame) -> pd.DataFrame:
    keep_columns = list(filter(keep_column, df_source.columns))

    return df_source[keep_columns]


df_tracks = pd.merge(
    left=read_table(
        'tracks',
        create_engine(
            'sqlite:///{}/tracks.vdb'.format(database_directory)
        )
    ),
    right=read_table(
        'tracks',
        create_engine(
            'sqlite:///{}/analysis.vdb'.format(database_directory)
        )
    ),
    how='inner',
    on='uid',
    suffixes=('', '_analysis')
)


df_trackways = pd.merge(
    left=read_table(
        'trackways',
        create_engine(
            'sqlite:///{}/tracks.vdb'.format(database_directory)
        )
    ),
    right=read_table(
        'trackways',
        create_engine(
            'sqlite:///{}/analysis.vdb'.format(database_directory)
        )
    ),
    how='inner',
    on='index',
    suffixes=('', '_analysis')
)

df_tracks = df_tracks.query('site == "BEB" and level == "500"')
df_tracks = purge_columns(df_tracks)

cd.display.markdown(
    """
    # Cadence Data

    The source data used for this export process comes from four tables in the
    Cadence database, the tracks and trackways tables and their analysis
    counterparts. The tables and their analysis counterparts were joined into
    two tables, one for tracks and one for trackways. The following is a
    partial printing of each table for reference.
    """
)

cd.display.header('Tracks (First 100 Entries)', 2)
cd.display.table(df_tracks.head(100), 0.3)

df_trackways = df_trackways[df_trackways['name'].str.startswith('BEB-500')]
df_trackways = purge_columns(df_trackways)

cd.display.header('Trackways', 2)
cd.display.table(df_trackways, 0.3)

cd.shared.df_tracks = df_tracks
cd.shared.df_trackways = df_trackways
