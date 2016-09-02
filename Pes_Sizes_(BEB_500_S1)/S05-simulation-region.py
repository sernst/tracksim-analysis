import cauldron as cd
import numpy as np

df = cd.shared.df

lp_region = [11, 22]
rp_region = [10, 22]
lm_region = [12, 24]
rm_region = [11, 23]

lp_df = df[
    (df['lp_track'] >= lp_region[0]) &
    (df['lp_track'] <= lp_region[1])
]

rp_df = df[
    (df['rp_track'] >= rp_region[0]) &
    (df['rp_track'] <= rp_region[1])
]

pes_length = cd.shared.calculate_median(
    np.concatenate((lp_df['lp_l'].values, rp_df['rp_l'].values)),
    np.concatenate((lp_df['lp_dl'].values, rp_df['rp_dl'].values))
)

pes_width = cd.shared.calculate_median(
    np.concatenate((lp_df['lp_w'].values, rp_df['rp_w'].values)),
    np.concatenate((lp_df['lp_dw'].values, rp_df['rp_dw'].values))
)

lm_df = df[
    (df['lm_track'] >= lp_region[0]) &
    (df['lm_track'] <= lp_region[1])
]

rm_df = df[
    (df['rm_track'] >= rp_region[0]) &
    (df['rm_track'] <= rp_region[1])
]

manus_length = cd.shared.calculate_median(
    np.concatenate((lp_df['lm_l'].values, rp_df['rm_l'].values)),
    np.concatenate((lp_df['lm_dl'].values, rp_df['rm_dl'].values))
)

manus_width = cd.shared.calculate_median(
    np.concatenate((lp_df['lm_w'].values, rp_df['rm_w'].values)),
    np.concatenate((lp_df['lm_dw'].values, rp_df['rm_dw'].values))
)

cd.display.markdown(
    """
    Simulation Region
    =================

    The following are the results for the part of the trackway used in coupling
    length simulations (cycles 9.5 - 21), which translate into tracks:

    * Left Pes: **LP{{ lp_region[0] }} - LP{{ lp_region[1] }}**
    * Right Pes: **RP{{ rp_region[0] }} - RP{{ rp_region[1] }}**
    * Left Manus: **LM{{ lm_region[0] }} - LM{{ lm_region[1] }}**
    * Right Manus: **RM{{ rm_region[0] }} - RM{{ rm_region[1] }}**

    It should be noted that not all simulations use all tracks for each limb.
    Longer coupling length trials do not typically include the first manus
    prints for one or both manus limbs. And smaller coupling length trials
    often omit one or both of the last manus tracks.

    * Pes Width: **{{ pes_width.html_label }} m**
    * Pes Length: **{{ pes_length.html_label }} m**
    * Manus Width: **{{ manus_width.html_label }} m**
    * Manus Length: **{{ manus_length.html_label }} m**
    """,
    pes_length=pes_length,
    pes_width=pes_width,
    manus_length=manus_length,
    manus_width=manus_width,
    lp_region=lp_region,
    rp_region=rp_region,
    lm_region=lm_region,
    rm_region=rm_region
)
