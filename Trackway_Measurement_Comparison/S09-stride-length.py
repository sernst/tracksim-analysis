import cauldron as cd
import pandas as pd

generate_data = cd.shared.generate_data
get_analyzer_results = cd.shared.get_analyzer_results

df = pd.merge(
    get_analyzer_results(
        'ValidationAnalyzer',
        'Stride-Length-Deviations.csv',
        renames={'UID': 'uid'}
    ),
    cd.shared.df_tracks[['uid', 'site', 'width', 'size_class']],
    left_on='uid',
    right_on='uid'
)

stride_data = generate_data(
    name='stride',
    key='Deviation',
    df=df.query('Deviation >= 0.0'),
    bin_count=10.0
)

cd.shared.plot_remainder(
    data=stride_data,
    key='stride',
    label='Stride',
    is_log=False
)

cd.shared.plot_remainder(
    data=stride_data,
    key='stride',
    label='Stride',
    is_log=True
)
