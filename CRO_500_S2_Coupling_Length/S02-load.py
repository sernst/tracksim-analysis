import cauldron as cd
from tracksim.coupling import loader as tk_loader

cd.watch(tk_loader)

data = tk_loader.load([
    'CRO-500-2004-3-S-2_v0_full_dc50',
    'CRO-500-2004-3-S-2_v0_full',
    'CRO-500-2004-3-S-2_v0_full_dc75'
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
