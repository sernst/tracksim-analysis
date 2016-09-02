import os

import cauldron as cd
import pandas as pd

DATA_PATH = os.path.join(
    os.path.expanduser('~'),
    'Dropbox',
    'A16',
    'Notebook-Data',
    'trackway-data',
    'BEB',
    'BEB-500-2014-1-S-1.csv'
)

df = pd.read_csv(DATA_PATH)

drop_columns = [
    c for c in df.columns
    if c.split('_')[-1] in ['x', 'dx', 'y', 'dy']
]

df = df.drop(drop_columns, axis=1)

for prefix in ['lp', 'rp', 'lm', 'rm']:
    src_name = '{}_name'.format(prefix)
    out_name = '{}_track'.format(prefix)
    df[out_name] = df[src_name].str.split('-').str[-1]
    df[out_name] = df[out_name].convert_objects(convert_numeric=True)

cd.shared.df = df

cd.display.table(df)
