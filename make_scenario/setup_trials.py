import os
import json

import cauldron as cd

path = cd.shared.target_path

for item in os.listdir(path):

    # just work on the trials
    if item == 'group.json' or not item.endswith('.json'):
        continue

    item_path = os.path.join(path, item)
    cd.display.text(item_path)

    with open(item_path, mode='r+') as f:
        d = json.load(f)

    d["data"] = cd.shared.data
    d["steps_per_cycle"] = cd.shared.steps_per_cycle
    d["duty_cycle"] = cd.shared.duty_cycle

    # build unique trial name key starting with the full
    # gaitname (e.g., G5-trottingAmble2).  Verbose, but clear.
    ga = item.split('.')[0]
    tn = cd.shared.trackway_name
    sn = cd.shared.scenario_name

    name = '{}_{}_{}'.format(ga, tn, sn)

    if cd.shared.start_time:
        st = cd.shared.start_time
        d["start_time"] = st

    if cd.shared.end_time:
        et = cd.shared.end_time
        d["end_time"] = et

    print(name)
    d["name"] = name
    # save with 2-space indents
    with open(item_path, mode='w+') as f:
        json.dump(d, f, indent=2, sort_keys=True)
