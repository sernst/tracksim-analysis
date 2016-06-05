from tracksim import reader as tk_reader

import cauldron as cd

data = tk_reader.groups(
    'Generated-Regular_*',
    load_trials=True
)

for item in data['groups'] + data['trials']:
    item['collection'] = 'ideal'

s21 = tk_reader.group(
    'BEB-515-2009-1-S-21_v0_st9_et21',
    load_trials=True
)
s21['group']['collection'] = 'S21'
for item in s21['trials']:
    item['collection'] = 'S21'
data['groups'] += s21['group']
data['trials'] += s21['trials']

s1 = tk_reader.group(
    'BEB-500-2014-1-S-1_v0_st9point5_et21',
    load_trials=True
)
s1['group']['collection'] = 'S4'
for item in s1['trials']:
    item['collection'] = 'S4'
data['groups'] += s1['group']
data['trials'] += s1['trials']

cd.shared.data = data
