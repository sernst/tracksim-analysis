import cauldron as cd
import pandas as pd
from cauldron import plotting
import measurement_stats as mstats

df = cd.shared.df  # type: pd.DataFrame
group = cd.shared.group

df = df[df.gait_id == 'G2'].sort_values(by='coupling_length')

for trial_id in df.id:
    for t in group['trials']:
        if t['id'] == trial_id:
            break

    data = t['couplings']['lengths']
    x = [v['time'] for v in data]

    couplings = mstats.values.from_serialized(
        [v['value'] for v in data]
    )

    y, unc = mstats.values.unzip(couplings)

    plot = plotting.make_line_data(
        x=x,
        y=y,
        y_unc=unc
    )

    cd.display.plotly(
        data=plot['data'],
        layout=plotting.create_layout(
            plot['layout'],
            title='{} Coupling Length'.format(t['id'].split('_', 1)[0]),
            x_label='Cycle (#)',
            y_label='Coupling Length (m)'
        )
    )

    min_value = mstats.values.minimum(couplings)
    cd.display.html('<div>Min: {} m</div>'.format(min_value.html_label))

    median = mstats.ValueUncertainty()
    median.from_dict(t['couplings']['value'])
    cd.display.html('<div>Median: {} m</div>'.format(median.html_label))

    max_value = mstats.values.maximum(couplings)
    cd.display.html('<div>Max: {} m</div>'.format(max_value.html_label))

    deviation = 100.0 * (max_value - min_value) / median
    cd.display.html('<div>Swing: {}%</div>'.format(deviation.html_label))
