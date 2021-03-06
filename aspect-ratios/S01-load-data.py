import os
import glob

import cauldron as cd
import pandas as pd
import measurement_stats as mstats


glob_path = os.path.expanduser(os.path.join(
    '~', 'Dropbox', 'A16', 'Notebook-Data', 'trackway-data', '**', '*.csv'
))

data_frames = []

for item_path in glob.iglob(glob_path, recursive=True):
    df = pd.read_csv(item_path)
    trackway_name = item_path.split(os.path.sep)[-1].split('.')[0]
    parts = trackway_name.split('-')
    df['trackway'] = trackway_name
    df['site'] = parts[0]
    df['level'] = parts[1]
    df['year'] = parts[2]
    df['sector'] = '-'.join(parts[3:-2])
    df['number'] = parts[-1]
    data_frames.append(df)


tracks_df = pd.concat(data_frames, ignore_index=True)

cd.shared.tracks_df = tracks_df
cd.display.table(tracks_df.head())

