import cauldron as cd
import pandas as pd


def pace_length_data():
    """

    :return:
    """

    df = pd.merge(
        get_analysis_data(
            'ValidationAnalyzer',
            'Pace-Length-Deviations.csv',
            renames={'UID': 'uid'}
        ),
        cd.shared.df_tracks[['uid', 'site', 'width', 'sizeClass']],
        on='uid'
    )

    return dict(
        df=df,
        pace_data=generate_data('pace', df, 'Deviation', 10.0)
    )
