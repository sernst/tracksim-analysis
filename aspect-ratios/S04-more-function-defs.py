import cauldron as cd
import measurement_stats as mstats
import plotly.graph_objs as go
from cauldron import plotting


def create_density_trace(dist, color_index=0, name=None):
    x = mstats.distributions.adaptive_range(dist, 5)
    y = dist.probabilities_at(x)

    return go.Scatter(
        x=x,
        y=y,
        name=name,
        fill='tozeroy',
        mode='lines',
        line=dict(
            color=plotting.get_color(color_index)
        )
    )
cd.shared.create_density_trace = create_density_trace


def get_trackway_row(trackway_name):
    df = cd.shared.trackway_df
    return df[df['name'] == trackway_name].iloc[0]
cd.shared.get_trackway_row = get_trackway_row


def print_track_counts(trackway_df):
    counts = [
        trackway_df['lp_count'].sum(),
        trackway_df['rp_count'].sum(),
        trackway_df['lm_count'].sum(),
        trackway_df['rm_count'].sum()
    ]

    cd.display.listing([
        'Left Pes: {}'.format(counts[0]),
        'Right Pes: {}'.format(counts[1]),
        'Left Manus: {}'.format(counts[2]),
        'Right Manus: {}'.format(counts[3]),
        'Total: {}'.format(sum(counts))
    ])
    return counts
cd.shared.print_track_counts = print_track_counts


def plot_pes_aspects(trackway_df):
    measurements = mstats.values.join(
        trackway_df['pes_aspect'].tolist(),
        trackway_df['pes_daspect'].tolist()
    )

    dist = mstats.create_distribution(
        [x for x in measurements if x.value > 0]
    )

    pop = mstats.distributions.population(dist)
    median = mstats.ValueUncertainty(
        mstats.distributions.percentile(pop),
        mstats.distributions.weighted_median_average_deviation(pop)
    )

    cd.display.plotly(
        cd.shared.create_density_trace(dist),
        plotting.create_layout(
            {},
            title='Pes Aspect Ratio Distribution (by trackway)',
            x_label='Aspect Ratio (width / length)',
            y_label='Probability Density'
        )
    )

    print('Median Pes Aspect Ratio:', median.label)

cd.shared.plot_pes_aspects = plot_pes_aspects


def plot_pes_aspects_by_tracks(tracks_df):
    widths = cd.shared.to_measurements(tracks_df, ['lp', 'rp'], 'w')
    lengths = cd.shared.to_measurements(tracks_df, ['lp', 'rp'], 'l')
    measurements = [l / w for l, w in zip(lengths, widths)]

    dist = mstats.create_distribution(
        [x for x in measurements if x.value > 0]
    )

    pop = mstats.distributions.population(dist)
    median = mstats.ValueUncertainty(
        mstats.distributions.percentile(pop),
        mstats.distributions.weighted_median_average_deviation(pop)
    )

    cd.display.plotly(
        cd.shared.create_density_trace(dist),
        plotting.create_layout(
            {},
            title='Pes Aspect Ratio Distribution (by track)',
            x_label='Aspect Ratio (width / length)',
            y_label='Probability Density'
        )
    )

    print('Median Pes Aspect Ratio:', median.label)

cd.shared.plot_pes_aspects_by_tracks = plot_pes_aspects_by_tracks


def plot_sizes(trackway_df, pes=True):
    prefix = 'pes' if pes else 'manus'
    length_measurements = mstats.values.join(
        trackway_df['{}_l'.format(prefix)].tolist(),
        trackway_df['{}_dl'.format(prefix)].tolist()
    )
    length_dist = mstats.create_distribution(
        [x for x in length_measurements if x.value > 0]
    )
    pop = mstats.distributions.population(length_dist)
    length_median = mstats.ValueUncertainty(
        mstats.distributions.percentile(pop),
        mstats.distributions.weighted_median_average_deviation(pop)
    )

    width_measurements = mstats.values.join(
        trackway_df['{}_w'.format(prefix)].tolist(),
        trackway_df['{}_dw'.format(prefix)].tolist()
    )
    width_dist = mstats.create_distribution(
        [x for x in width_measurements if x.value > 0]
    )
    pop = mstats.distributions.population(width_dist)
    width_median = mstats.ValueUncertainty(
        mstats.distributions.percentile(pop),
        mstats.distributions.weighted_median_average_deviation(pop)
    )

    label = prefix.capitalize()

    cd.display.plotly(
        [
            cd.shared.create_density_trace(length_dist, 0, 'Length'),
            cd.shared.create_density_trace(width_dist, 1, 'Width'),
        ],
        plotting.create_layout(
            {},
            title='{} Width & Length Distributions (by trackway)'.format(label),
            x_label='Size (m)',
            y_label='Probability Density'
        )
    )

    print('Median {} Width: {}m'.format(label, width_median.label))
    print('Median {} Length: {}m'.format(label, length_median.label))

cd.shared.plot_sizes = plot_sizes


def plot_sizes_by_track(tracks_df, pes=True):
    prefix = 'pes' if pes else 'manus'
    limb_ids = ['lp', 'rp'] if pes else ['lm', 'rm']

    length_measurements = cd.shared.to_measurements(tracks_df, limb_ids, 'l')
    length_dist = mstats.create_distribution(
        [x for x in length_measurements if x.value > 0]
    )
    pop = mstats.distributions.population(length_dist)
    length_median = mstats.ValueUncertainty(
        mstats.distributions.percentile(pop),
        mstats.distributions.weighted_median_average_deviation(pop)
    )

    width_measurements = cd.shared.to_measurements(tracks_df, limb_ids, 'w')
    width_dist = mstats.create_distribution(
        [x for x in width_measurements if x.value > 0]
    )
    pop = mstats.distributions.population(width_dist)
    width_median = mstats.ValueUncertainty(
        mstats.distributions.percentile(pop),
        mstats.distributions.weighted_median_average_deviation(pop)
    )

    label = prefix.capitalize()

    cd.display.plotly(
        [
            cd.shared.create_density_trace(length_dist, 0, 'Length'),
            cd.shared.create_density_trace(width_dist, 1, 'Width'),
        ],
        plotting.create_layout(
            {},
            title='{} Width & Length Distributions (by track)'.format(label),
            x_label='Size (m)',
            y_label='Probability Density'
        )
    )

    print('Median {} Width: {}m'.format(label, width_median.label))
    print('Median {} Length: {}m'.format(label, length_median.label))

cd.shared.plot_sizes_by_track = plot_sizes_by_track
