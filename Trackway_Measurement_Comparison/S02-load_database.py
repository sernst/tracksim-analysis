import os
import cauldron as cd
from sqlalchemy import create_engine
import pandas as pd
import re

database_directory = os.path.join(
    cd.shared.ROOT_PATH,
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


def size_class_mapper(track_width):
    """

    :param track_width:
    :return:
    """

    for size_class in cd.shared.SIZE_CLASSES:
        if track_width >= size_class['range'][1]:
            continue
        return size_class['index']
    return -1


df = pd.merge(
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

df['size_class'] = df['width'].map(size_class_mapper)

cd.shared.df_tracks = df
