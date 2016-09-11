import cauldron


def stride_length_data():
    """

    :return:
    """

    df = pd.merge(
        get_analysis_data(
            'ValidationAnalyzer',
            'Stride-Length-Deviations.csv',
            renames={'UID': 'uid'}
        ),
        cd.shared.df_tracks[['uid', 'site', 'width', 'sizeClass']],
        on='uid'
    )

    stride_data = generate_data('stride', df, 'Deviation', 10.0)

    return dict(
        df=df,
        stride_data=stride_data,
    )
