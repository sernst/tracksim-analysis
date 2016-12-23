import glob
import os

import cauldron as cd
import pandas as pd

from _measurement_uncertainty import loading
from _measurement_uncertainty import trackways

MIN_TRACK_THRESHOLD = 10

glob_path = os.path.expanduser(os.path.join(
    '~', 'Dropbox', 'A16', 'Notebook-Data', 'trackway-data', '**', '*.csv'
))
csv_paths = list(glob.iglob(glob_path, recursive=True))


def load_csv(csv_path: str) -> list:
    cd.display.status(
        progress=(1 + csv_paths.index(csv_path)) / len(csv_paths)
    )
    return loading.load_csv(csv_path, MIN_TRACK_THRESHOLD)


tracks_df = (
    pd.DataFrame([
        track
        for path in csv_paths
        for track in load_csv(path)
    ])
    .sort_values(by='trackway')
)


def create_trackway_info(
        trackway_name: str,
        trackway_df: pd.DataFrame,
        **kwargs
) -> dict:
    """
    Creates information about the trackway
    """

    pes_df = trackway_df.query('is_pes == True')
    manus_df = trackway_df.query('is_pes == False')

    return dict(
        trackway=trackway_name,
        pes_count=len(pes_df),
        manus_count=len(manus_df)
    )

trackway_info_df = pd.DataFrame(
    list(trackways.for_each(create_trackway_info, tracks_df).values())
)

cd.display.markdown(
    """
    ## A16 Data

    Of the complete A16 data set, only trackways that contain at least
    {{ MIN_TRACK_THRESHOLD }} pes tracks are included in this investigation.
    We have eliminated short trackways because they provide an insufficient
    amount of data for statistical analysis.

    The resulting data contains:

     * {{ track_count }} tracks
     * {{ trackway_count }} trackways

    which is a sufficient sample size for the purposes of this investigation.
    The {{ trackway_count }} trackways in the data set are:
    """,
    track_count=len(tracks_df),
    trackway_count=len(trackway_info_df),
    MIN_TRACK_THRESHOLD=MIN_TRACK_THRESHOLD
)

cd.display.table(trackway_info_df, 0.4)


cd.shared.tracks_df = tracks_df
