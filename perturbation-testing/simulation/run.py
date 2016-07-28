import os
import shutil
import random
import json
import pandas as pd

from tracksim import paths
from tracksim import scenario
from tracksim.group import simulate

MY_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

paths.override('results', os.path.join(MY_DIRECTORY, 'results'))

source_path = os.path.join(MY_DIRECTORY, 'scenarios')
ideal_data_path = os.path.join(MY_DIRECTORY, 'data.csv')

settings = []


def create_perturbed_source(save_path, delta_x, delta_y):
    """

    :return:
    """

    df = pd.read_csv(ideal_data_path)
    out = []

    for index, row in df.iterrows():
        row = row.to_dict()
        row['lp_x'] += random.uniform(-delta_x, delta_x)
        row['lp_y'] += random.uniform(-delta_y, delta_y)
        row['rp_x'] += random.uniform(-delta_x, delta_x)
        row['rp_y'] += random.uniform(-delta_y, delta_y)
        row['lm_x'] += random.uniform(-delta_x, delta_x)
        row['lm_y'] += random.uniform(-delta_y, delta_y)
        row['rm_x'] += random.uniform(-delta_x, delta_x)
        row['rm_y'] += random.uniform(-delta_y, delta_y)
        out.append(row)

    pd.DataFrame(out).to_csv(save_path)


for i in range(20):
    trackway_name = '5PP'
    scenario_name = 'trial-{}'.format(i + 1)
    scenario_path = os.path.join(source_path, trackway_name, scenario_name)

    if os.path.exists(scenario_path):
        shutil.rmtree(scenario_path)

    scenario.create(
        trackway_name=trackway_name,
        scenario_name=scenario_name,
        root_path=source_path,
        data_filename='generated.csv',
        duty_cycle=0.6
    )

    create_perturbed_source(
        os.path.join(scenario_path, 'generated.csv'),
        0.05,
        0.05
    )

    group_path = os.path.join(scenario_path, 'group.json')
    with open(group_path, 'r') as f:
        group_settings = json.load(f)

    url = simulate.run(group_path)

    print(url)
    group_settings['url'] = url
    settings.append(group_settings)

print('FINISHED:')
for s in settings:
    print('* {}'.format(s['url']))

