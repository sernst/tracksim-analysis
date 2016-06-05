import re

import pandas as pd
import measurement_stats as mstats
import cauldron as cd

couplings_data = cd.shared.couplings_data

rows = []

for entry in couplings_data:
    id_parts = entry['id'].split('_')
    gait_parts = id_parts[0].split('-', 2)
    gait_id = gait_parts[0]
    gait_number = re.sub(r'[^0-9]+', '', gait_parts[1]).strip()
    gait_number = int(gait_number) if len(gait_number) > 0 else 1

    if entry['trial']['collection'] == 'ideal':
        print_interval = 0.01 * float(id_parts[3])
    else:
        print_interval = -1.0

    out = dict(
        uid=entry['id'],
        collection=entry['trial']['collection'],
        gait=id_parts[0],
        gait_id=gait_id,
        phase_id=int(gait_id[1:]),
        gait_name=re.sub(r'[0-9]+', '', gait_parts[1]),
        gait_number=gait_number,
        print_interval=print_interval,
        duty_cycle=entry['trial']['settings']['duty_cycle']
    )

    sources = dict(
        raw=entry['couplings'],
        smooth=entry['smooth_couplings']
    )

    for prefix, couplings in sources.items():
        d = mstats.Distribution(entry['couplings'])
        pop = mstats.distributions.population(d)
        median = mstats.distributions.percentile(pop)
        mad = mstats.distributions.weighted_median_average_deviation(pop)
        values, uncertainties = mstats.values.unzip(d.measurements)
        maximum = max(*values)
        minimum = min(*values)
        swing = maximum - minimum
        fractional_swing = swing / median

        out['{}_median'.format(prefix)] = median
        out['{}_mad'.format(prefix)] = mad
        out['{}_max'.format(prefix)] = maximum
        out['{}_min'.format(prefix)] = minimum
        out['{}_swing'.format(prefix)] = swing
        out['{}_fractional_swing'.format(prefix)] = fractional_swing

    rows.append(out)

df = pd.DataFrame(rows).sort_values(by='uid')
cd.shared.couplings_df = df
