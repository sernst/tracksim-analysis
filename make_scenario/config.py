import os
import cauldron as cd

#cd.shared.trackway_name = "BEB-515-2009-1-S-21"
cd.shared.trackway_name = "BEB-500-2014-1-S-4"

cd.shared.scenario_name = "v0_full"
#cd.shared.scenario_name = "v0_st9_et21"
#cd.shared.scenario_name = "v0_st9p5_et21"
#cd.shared.scenario_name = "v0_st10_et21"

# the following are optional
#cd.shared.start_time = 9
#cd.shared.end_time = 21

# the CSV file containing trackway data
cd.shared.data = "scenario.csv"

cd.shared.root_path =  os.path.expanduser("~/Dropbox/A16/Simulation")

# default values for trials, to be applied to all trials in a given group
cd.shared.steps_per_cycle = 20
cd.shared.duty_cycle = 0.6

