import cauldron as cd
from tracksim.coupling import loader as tk_loader

cd.refresh(tk_loader)

data = tk_loader.load([
    'BEB-500-2014-1-S-3_v0_st9p5_end_dc_50',
    'BEB-500-2014-1-S-3_v0_st9p5_end',
    'BEB-500-2014-1-S-3_v0_st9p5_end_dc_75'
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
