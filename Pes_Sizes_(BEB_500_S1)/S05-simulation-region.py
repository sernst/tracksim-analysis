import cauldron as cd
from cauldron import plotting
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
    np.concatenate((lp_df['lp_dl'].values, rp_df['rp_dl'].values)),
    plot_name='Width',
    color_index=1
)

pes_width = cd.shared.calculate_median(
    np.concatenate((lp_df['lp_w'].values, rp_df['rp_w'].values)),
    np.concatenate((lp_df['lp_dw'].values, rp_df['rp_dw'].values)),
    plot_name='Length',
    color_index=0
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
    np.concatenate((lp_df['lm_dl'].values, rp_df['rm_dl'].values)),
    plot_name='Width',
    color_index=3
)

manus_width = cd.shared.calculate_median(
    np.concatenate((lp_df['lm_w'].values, rp_df['rm_w'].values)),
    np.concatenate((lp_df['lm_dw'].values, rp_df['rm_dw'].values)),
    plot_name='Length',
    color_index=2
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
    """,
    lp_region=lp_region,
    rp_region=rp_region,
    lm_region=lm_region,
    rm_region=rm_region
)

cd.display.plotly(
    data=[
        pes_width['trace'],
        pes_length['trace']
    ],
    layout=plotting.create_layout(
        title='Pes Width: {} m & Length: {} m'.format(
            pes_width['median'].html_label,
            pes_length['median'].html_label
        ),
        x_label='Size (m)',
        y_label='Probability Density (AU)'
    )
)

cd.display.plotly(
    data=[
        manus_width['trace'],
        manus_length['trace']
    ],
    layout=plotting.create_layout(
        title='Manus Width: {} m & Length: {} m'.format(
            manus_width['median'].html_label,
            manus_length['median'].html_label
        ),
        x_label='Size (m)',
        y_label='Probability Density (AU)'
    )
)
