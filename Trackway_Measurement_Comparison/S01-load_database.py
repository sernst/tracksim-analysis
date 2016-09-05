import os
import cauldron as cd
from sqlalchemy import create_engine

data_directory = os.path.join(
    os.path.expanduser('~'),
    'Dropbox',
    'A16',
    'Notebook-Data',
    'cadence-databases'
)

tracks_engine = create_engine(
    'sqlite:///{}/tracks.vdb'.format(data_directory)
)

analysis_engine = create_engine(
    'sqlite:///{}/analysis.vdb'.format(data_directory)
)

cd.shared.put(
    tracks_engine=tracks_engine,
    analysis_engine=analysis_engine
)

