import measurement_stats as mstats
import cauldron as cd

data = cd.shared.data

couplings_data = []

for trial in data['trials']:
    measurements = mstats.values.from_serialized(
        trial['couplings']['lengths']
    )

    smoothed_measurements = mstats.values.windowed_smooth(
        measurements,
        size=5,
        population_size=256
    )

    couplings_data.append(dict(
        id=trial['id'],
        trial=trial,
        couplings=measurements,
        smooth_couplings=smoothed_measurements
    ))

cd.shared.couplings_data = couplings_data
