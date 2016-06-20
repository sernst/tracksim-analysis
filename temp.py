import os
import json

root_path = '/Users/scott/Dropbox/A16/Simulation/scenarios'

slugs = [
    'BEB-500-2014-1-S-1/v0_st10_et21/G4-trot2.json',
    'BEB-500-2014-1-S-1/v0_st9point5_et21/G4-trot2.json',
    'BEB-500-2014-1-S-2/group_st20_et40_v0/G4-trot2.json',
    'BEB-500-2014-1-S-2/scenario_v1/G4-trot2.json',
    'BEB-500-2014-1-S-3/scenario_v0/G4-trot2.json',
    'BEB-500-2014-1-S-4/v0_full/G4-trot2.json',
    'BEB-500-2014-1-S-7/v0/G4-trot2.json',
    'BEB-515-2009-1-S-18/scenario_v0/G4-trot2.json',
    'BEB-515-2009-1-S-18/v0_full/G4-trot2.json',
    'BEB-515-2009-1-S-18/v0_st0_et20/G4-trot2.json',
    'BEB-515-2009-1-S-19/scenario_v0/G4-trot2.json',
    'BEB-515-2009-1-S-19/v0_full/G4-trot2.json',
    'BEB-515-2009-1-S-19/v0_st0_et20/G4-trot2.json',
    'BEB-515-2009-1-S-21/v0_full/G4-trot2.json',
    'BEB-515-2009-1-S-21/v0_st0_et5/G4-trot2.json',
    'BEB-515-2009-1-S-21/v0_st0p5_et5/G4-trot2.json',
    'BEB-515-2009-1-S-21/v0_st9_et21/G4-trot2.json',
    'BEB-600-2010-6-S-7/scenario_v0/G4-trot2.json',
    'Generated-Regular/PI_0_DC_60/G4-trot2.json',
    'Generated-Regular/PI_0_DC_75/G4-trot2.json',
    'Generated-Regular/PI_25_DC_60/G4-trot2.json',
    'Generated-Regular/PI_25_DC_75/G4-trot2.json',
    'Generated-Regular/PI_50_DC_60/G4-trot2.json',
    'Generated-Regular/PI_50_DC_75/G4-trot2.json',
    'Generated-Regular/PI_75_DC_60/G4-trot2.json',
    'Generated-Regular/PI_75_DC_75/G4-trot2.json',
    'SCR-1000-2008-18-S-1/scenario_v0/G4-trot2.json',
    'SCR-1000-2008-18-S-22/scenario_v0/G4-trot2.json',
    'SCR-1000-2008-18-S-27/scenario_v0/G4-trot2.json',
    'TCH-1030-2006-12-S-4/scenario_v0/G4-trot2.json',
    'TST-500-2016-1-S-1/v0/G4-trot2.json'
]

for s in slugs:
    p = os.path.join(root_path, s)
    with open(p, 'r+') as f:
        data = json.load(f)

    data['support_phases'] = [0, 0.5, -2.5, -2.0]

    with open(p, 'w+') as f:
        json.dump(data, f, indent=2, sort_keys=True)

    print('FIXED:', s)

print('Operation Complete')
