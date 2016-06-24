import pandas as pd
import cauldron as cd
import numpy as np

from tracksim import reader as tk_reader

group = tk_reader.group('BEB-500-2014-1-S-1_v0_st9p5_et21')

cd.shared.group = group

df = []
for t in group['trials']:
    gait_id, remainder = t['id'].split('-', 1)
    gait_name = remainder.split('_', 1)[0]
    try:
        separation = int(gait_name[-1])
        gait_name = gait_name[:-1]
    except Exception:
        separation = 1

    df.append(dict(
        id=t['id'],
        gait_id=gait_id,
        gait_name=gait_name,
        separation=separation,
        coupling_length=t['couplings']['value']['value'],
        uncertainty=t['couplings']['value']['uncertainty']
    ))

df = pd.DataFrame(df).sort_values(by='coupling_length')
df['order'] = np.arange(0, df.shape[0], 1)

cd.shared.df = df

cd.display.table(df)
