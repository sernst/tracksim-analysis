import json

import cauldron as cd
from tracksim import paths as tk_paths

GROUP_ID = 'BEB-500_S1-scenario-v0'

group_data_path = tk_paths.results(
    'reports', 'group',
    GROUP_ID,
    '{}.json'.format(GROUP_ID)
)

with open(group_data_path, 'r+') as f:
    group_data = json.load(f)

trials = []
for trial_data in group_data['trials']:
    trial_path = tk_paths.results(
        'reports', 'trial',
        trial_data['id'],
        '{}.json'.format(trial_data['id'])
    )

    with open(trial_path, 'r+') as f:
        trials.append(json.load(f))

cd.shared.group = group_data
cd.shared.trials = trials

cd.display.header('Trial Data Structure:')
cd.display.inspect(trials[0])
