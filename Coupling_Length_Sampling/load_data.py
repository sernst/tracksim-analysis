import re

import cauldron as cd
import pandas as pd
from tracksim import reader as tk_reader

group_ids = [
    'Generated-Regular_PI_25_DC_60',
    'Generated-Regular_PI_25_DC_75'
]

groups = [tk_reader.group(gid) for gid in group_ids]

trials = []
for g in groups:
    trials += g['trials']

df_data = []
for trial in trials:
    gait_id, section = trial['id'].split('-', 1)
    section = section.split('_', 1)[0]
    gait_name = re.compile('[0-9]+').sub('', section)

    try:
        spacing = int(re.compile('[^0-9]+').sub('', section))
    except ValueError:
        spacing = 1

    df_data.append(dict(
        id=trial['id'],
        duty_cycle=trial['settings']['duty_cycle'],
        gait_id=gait_id,
        gait_name=gait_name,
        spacing=spacing,
        CL=trial['couplings']['value']['value'],
        deltaCL=trial['couplings']['value']['uncertainty']
    ))

df = pd.DataFrame(df_data)


cd.display.markdown(
"""
The following groups have been loaded for this investigation:

{groups}

the trials of which are shown in the following table:
""".format(
    groups='\n'.join(['   * {}'.format(gid) for gid in group_ids])
))
cd.display.table(df)

cd.shared.df = df
cd.shared.trials = trials

