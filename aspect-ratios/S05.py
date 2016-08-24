import cauldron as cd
import measurement_stats as mstats

df = cd.shared.df
df = df[
    (df['site'] == 'BEB') &
    (df['level'] == '500')
]

def calculate_median(data):
    dist = mstats.create_distribution(data)
    population = mstats.distributions.population(dist)

    return mstats.ValueUncertainty(
        mstats.distributions.percentile(population),
        mstats.distributions.weighted_median_average_deviation(population)
    )


for name in df['name'].unique():
    df_slice = df[df['name'] == name]
    widths = cd.shared.to_measurements(df_slice, ['lp', 'rp'], 'w')
    width_median = calculate_median(widths)

    lengths = cd.shared.to_measurements(df_slice, ['lp', 'rp'], 'l')
    length_median = calculate_median(lengths)

    aspects = []
    for l, w in zip(lengths, widths):
        aspects.append(l / w)

    aspect_median = calculate_median(aspects)

    cd.display.header(name, 3)
    print('  * Width:', width_median.label)
    print('  * Length:', length_median.label)
    print('  * Aspect:', aspect_median.label)

