import numpy as np
import cauldron as cd
from cauldron import plotting
import pandas as pd

from tracksim import paths
from tracksim import reader

paths.override('results', '../simulation/results')
data = reader.groups()

entries = []

for t in data['trials']:
    parts = t['id'].replace('_', '-').split('-')

    entries.append(dict(
        gait_id=parts[0],
        label='{}-{}'.format(*parts[:2]),
        rmsd=t['couplings']['rmsd'],
        swing=t['couplings']['swing'],
        color=plotting.get_color(int(parts[0][-1])),
        coupling_length=t['couplings']['value']['value'],
        uncertainty=t['couplings']['value']['uncertainty']
    ))

df = pd.DataFrame(entries).sort_values(by=['coupling_length', 'gait_id'])
df['order'] = np.arange(0, df.shape[0], 1)

cd.shared.df = df
cd.display.table(df)



