import cauldron as cd

cd.display.header('Length Comparisons', 2)

cd.shared.plot_remainder(
    data=cd.shared.length_data,
    key='length',
    label='Length',
    is_log=False
)

cd.shared.plot_remainder(
    data=cd.shared.length_data,
    key='length',
    label='Length',
    is_log=True
)
