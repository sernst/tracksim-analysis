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

trackway_name = 'BEB-515-2009-1-S-20'

engine = create_engine('sqlite:///{}/analysis.vdb'.format(database_directory))

df = pd.read_sql_query(
    sql='SELECT * FROM tracks WHERE trackwayName == "{}"'.format(trackway_name),
    con=engine
)

cd.display.table(df)
