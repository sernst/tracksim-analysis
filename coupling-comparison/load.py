import cauldron as cd
from tracksim import reader as tk_reader

GROUP_ID = 'BEB-500_S1-scenario-v0'

data = tk_reader.group(
    GROUP_ID,
    load_trials=True
)

cd.shared.group = data['group']
cd.shared.trials = data['trials']

cd.display.header('Trial Data Structure:')
cd.display.inspect(data['trials'][0])
