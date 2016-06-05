import cauldron as cd

df = cd.shared.couplings_df

for phase_id in df.phase_id.unique():

    sub_df = df[df.phase_id == phase_id]
