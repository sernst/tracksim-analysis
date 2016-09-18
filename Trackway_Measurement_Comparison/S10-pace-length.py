import cauldron as cd
import pandas as pd

generate_data = cd.shared.generate_data
get_analyzer_results = cd.shared.get_analyzer_results

df = pd.merge(
    get_analyzer_results(
        'ValidationAnalyzer',
        'Pace-Length-Deviations.csv',
        renames={'UID': 'uid'}
    ),
    cd.shared.df_tracks[['uid', 'site', 'width', 'size_class']],
    left_on='uid',
    right_on='uid'
)

pace_data = generate_data(
    name='pace',
    key='Deviation',
    df=df.query('Deviation >= 0.0'),
    bin_count=10.0
)

cdr_values = cd.shared.cdr_values_at(pace_data, [0, 2])

cd.display.markdown(
    """
    ## Pace Length

    * {{ y0 }}% with no deviation
    * {{ y2 }}% with a deviation < 200%
    """,
    y0=cdr_values[0]['label'],
    y2=cdr_values[2]['label']
)

cd.shared.plot_remainder(
    data=pace_data,
    key='pace',
    label='Pace',
    is_log=False
)

cd.shared.plot_remainder(
    data=pace_data,
    key='pace',
    label='Pace',
    is_log=True
)
