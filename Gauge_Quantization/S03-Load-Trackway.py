import os

import cauldron as cd
import pandas as pd
from sqlalchemy import create_engine

trackway_name = cd.shared.TRACKWAY_NAME

# The directory that contains the Cadence database files
database_directory = os.path.join(
    cd.shared.ROOT_PATH,
    'Notebook-Data',
    'cadence-databases'
)


def get_engine(database_name: str):
    """
    Create an SQLAlchemy engine for the specified Cadence database

    :param database_name:
        The name of the database to load without its vdb extension
    :return:
        An SQLAlchemy engine for the specified database
    """
    return create_engine('sqlite:///{}/{}.vdb'.format(
        database_directory,
        database_name
    ))


def get_tracks_analysis() -> pd.DataFrame:
    """
    Returns a data frame that contains analysis data entries for the
    tracks in the globally specified trackway.
    """

    query = 'SELECT * FROM tracks WHERE trackwayName == "{}"'.format(
        trackway_name
    )

    return pd.read_sql_query(query, con=get_engine('analysis'))


def get_tracks_source(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns a data frame that contains the source track information for each
    track in the globally specified trackway. The analysis tracks data frame
    is needed to load these tracks because the analysis tracks table includes
    a trackway name column but the source tracks table does not. Therefore, the
    uid values from the analysis tracks are used to determine which tracks to
    load from the source database.
    """

    uids = ','.join(['"{}"'.format(uid) for uid in df['uid']])
    query = 'SELECT * FROM tracks WHERE uid IN ({})'.format(uids)

    return pd.read_sql_query(query, con=get_engine('tracks'))


def load_tracks():
    """
    Creates a data frame with source and analysis track data for every track in
    the globally specified trackway.
    """

    df_analysis = get_tracks_analysis()

    return pd.merge(
        left=get_tracks_source(df_analysis),
        right=df_analysis,
        how='inner',
        on='uid',
        suffixes=('', '_analysis')
    )

cd.shared.tracks = load_tracks()
