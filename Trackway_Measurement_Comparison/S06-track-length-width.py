import cauldron as cd
import pandas as pd

generate_data = cd.shared.generate_data
get_analyzer_results = cd.shared.get_analyzer_results

df = pd.merge(
    get_analyzer_results(
        'ComparisonAnalyzer',
        'Length-Width-Deviations.csv',
        renames={
            'Width Deviation': 'widthDeviation',
            'Length Deviation': 'lengthDeviation',
            'Fingerprint': 'fingerprint',
            'UID': 'uid'
        }
    ),
    cd.shared.df_tracks[['uid', 'site', 'width', 'size_class']],
    left_on='uid',
    right_on='uid'
)

cd.shared.width_data = generate_data(
    name='width',
    key='widthDeviation',
    df=cd.shared.df_length_width.query('widthDeviation >= 0.0'),
    bin_count=10.0
)

cd.shared.length_data = generate_data(
    name='length',
    key='lengthDeviation',
    df=df.query('lengthDeviation >= 0.0'),
    bin_count=10.0
)

cd.display.header('Width Comparisons', 2)

cd.shared.plot_histogram(
    data=cd.shared.width_data,
    key='width',
    label='Width'
)



cd.shared.plot_histogram(
    data=width_data,
    key='width',
    label='Width',
    is_log=True
)

cd.shared.plot_remainder(
    data=width_data,
    key='width',
    label='Width',
    is_log=False
)

cd.shared.plot_remainder(
    data=width_data,
    key='width',
    label='Width',
    is_log=True
)
