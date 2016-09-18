import cauldron as cd
import pandas as pd
from collections import OrderedDict
import measurement_stats as mstats

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
    df=df.query('widthDeviation >= 0.0'),
    bin_count=10.0
)

cd.shared.length_data = generate_data(
    name='length',
    key='lengthDeviation',
    df=df.query('lengthDeviation >= 0.0'),
    bin_count=10.0
)

cd.display.markdown(
    """
    ## Width Comparisons

    We'll begin by looking at the track width measurements. The A16 data set has
    {{ count }} tracks where track width measurements were made both in the
    field and from maps. By calculating the deviation between measurement types
    for each of these tracks, the following distribution of deviations results:
    """,
    count=cd.shared.width_data['count']
)

cd.shared.plot_histogram(
    data=cd.shared.width_data,
    key='width',
    label='Width'
)

cd.display.markdown(
    """
    Deviations equal to or less than 200% are not considered statistically
    significant. The large majority of the tracks fall within this bounding
    region. Only a relatively few in percentage terms are have deviations in
    excess of 200%. The specific numbers are shown in the following table:
    """
)

df_all = cd.shared.width_data['sizes']['all']['df_histogram']
df = pd.DataFrame(OrderedDict(
    Bin=['{}%'.format(round(100 * x)) for x in df_all['x'].values],
    Count=df_all['y'],
    Percentage=[
        '{:0.3f}%'.format(100 * mstats.value.round_significant(x, 3))
        for x in df_all['y_fractional']
    ]
))
cd.display.table(df)

cd.display.markdown(
    """
    While familiar to many, histograms are not a sufficiently good way to
    analyze this data. Histograms generally suffer from binning problems,
    which can improperly represent the distribution of data they present.
    More specifically for this analysis, histograms make it difficult to compare
    the data distribution against an expectation distribution.
    """
)
