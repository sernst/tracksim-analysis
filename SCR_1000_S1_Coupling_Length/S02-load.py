import cauldron as cd
from tracksim.coupling import loader as tk_loader

cd.refresh(tk_loader)

data = tk_loader.load([
    'SCR-1000-2008-18-S-1_v0_st1_et8_dc50',
    'SCR-1000-2008-18-S-1_v0_st1_et8',
    'SCR-1000-2008-18-S-1_v0_st1_et8_dc75'
    ],
    row_filter=tk_loader.redundant_filter
)

cd.shared.groups = data['groups']
cd.shared.trials = data['trials']
cd.shared.df = data['df']

cd.display.table(data['df'][[
    'short_id', 'coupling_length', 'uncertainty',
    'start_time', 'end_time'
]])
