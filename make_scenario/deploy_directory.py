import os
import shutil
import json

import cauldron as cd

template_path = os.path.join(cd.shared.root_path, "template")

cd.shared.target_path = os.path.join(
    cd.shared.root_path,
    "scenarios",
    cd.shared.trackway_name,
    cd.shared.scenario_name)

if os.path.exists(cd.shared.target_path):
    raise FileExistsError('Scenario already exists')

trackway_path = os.path.dirname(cd.shared.target_path)

# create the scenario folder
if not os.path.exists(trackway_path):
    os.makedirs(trackway_path)

# copy the template version for each of the default trials
shutil.copytree(template_path, cd.shared.target_path)

# get group.json file and set it up.
print('path = {}'.format(cd.shared.target_path))
group_path = os.path.join(cd.shared.target_path, "group.json")

print('group_path is [{}]'.format(group_path))
if not os.path.exists(group_path):
    raise FileNotFoundError('group.json file not found')

with open(group_path, mode='r+') as f:
    d = json.load(f)

# set up the group's name key
d["name"] = '{}_{}'.format(cd.shared.trackway_name, cd.shared.scenario_name)

# save the group.json file with 2-space indents
with open(group_path, mode='w+') as f:
    json.dump(d, f, indent=2, sort_keys=True)