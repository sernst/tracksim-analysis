from tracksim import reader as tk_reader
import cauldron as cd

# TRIAL_ID = 'G2-walk_BEB-515-2009-1-S-21_v0_st9_et21'
TRIAL_ID = 'G2-walk_BEB-500-2014-1-S-1_v0_st9point5_et21'
# TRIAL_ID = 'G2-walk_BEB-500-2014-1-S-4_v0_full'
# TRIAL_ID = 'G2-walk2_BEB-500-2014-1-S-1_v0_st9point5_et21'

cd.shared.trial_id = TRIAL_ID
cd.shared.trial = tk_reader.trial(TRIAL_ID)
