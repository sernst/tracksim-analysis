import cauldron as cd
from tracksim.coupling import loader as tk_loader

cd.refresh(tk_loader)

data = tk_loader.load([
    'BEB-515-2009-1-S-21_v0_st8_et22_dc50',
    'BEB-515-2009-1-S-21_v0_st8_et22',
    'BEB-515-2009-1-S-21_v0_st8_et22_dc75'
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
