import cauldron as cd

trackway_df = cd.shared.trackway_df
trackway_df = trackway_df[
    (trackway_df['site'] == 'BEB') &
    (trackway_df['level'] == '500')
]
tracks_df = cd.shared.tracks_df
tracks_df = tracks_df[
    (tracks_df['site'] == 'BEB') &
    (tracks_df['level'] == '500')
]

cd.display.header('BEB 500')
cd.shared.print_track_counts(trackway_df)
cd.shared.plot_pes_aspects(trackway_df)
cd.shared.plot_pes_aspects_by_tracks(tracks_df)
cd.shared.plot_sizes(trackway_df, True)
cd.shared.plot_sizes_by_track(tracks_df, True)
cd.shared.plot_sizes(trackway_df, False)
cd.shared.plot_sizes_by_track(tracks_df, False)
