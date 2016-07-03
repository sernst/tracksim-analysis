import pandas as pd
import cauldron as cd
from cauldron import plotting
import numpy as np

from tracksim import reader as tk_reader

groups = [
    tk_reader.group('BEB-500-2014-1-S-1_v0_st9p5_et21_dc_50'),
    tk_reader.group('BEB-500-2014-1-S-1_v0_st9p5_et21'),
    tk_reader.group('BEB-500-2014-1-S-1_v0_st9p5_et21_dc_75')
]

trials = []
for g in groups:
    trials += g['trials']

cd.shared.groups = groups
cd.shared.trials = trials

df = []
for t in cd.shared.trials:
    gait_id, remainder = t['id'].split('-', 1)
    gait_name = remainder.split('_', 1)[0]

    try:
        separation = int(gait_name[-1])
        gait_name = gait_name[:-1]
    except Exception:
        separation = 1

    duty_cycle = int(100 * t['settings']['duty_cycle'])
    short_id = '{}-{} ({}%)'.format(gait_id, separation, duty_cycle)
    t['short_id'] = short_id

    df.append(dict(
        id=t['id'],
        short_id=short_id,
        duty_cycle=duty_cycle,
        gait_id=gait_id,
        gait_index=int(gait_id[1]),
        gait_name=gait_name,
        separation=separation,
        coupling_length=t['couplings']['value']['value'],
        uncertainty=t['couplings']['value']['uncertainty'],
        start_time=t['times']['cycles'][0],
        end_time=t['times']['cycles'][-1],
        color=plotting.get_color(int(gait_id[1]))
    ))

df = pd.DataFrame(df).sort_values(
    by=['coupling_length', 'gait_index', 'duty_cycle']
)
df['order'] = np.arange(0, df.shape[0], 1)
df['relative_uncertainty'] = df.uncertainty / df.coupling_length

cd.shared.df = df
cd.display.table(df[[
    'short_id', 'coupling_length', 'uncertainty',
    'start_time', 'end_time'
]])
