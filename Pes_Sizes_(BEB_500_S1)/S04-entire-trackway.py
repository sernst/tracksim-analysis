import cauldron as cd
import numpy as np
from cauldron import plotting
import measurement_stats as mstats

df = cd.shared.df


cd.display.markdown(
    """
    Entire Trackway
    ===============

    The following are the results for the entire trackway.
    """
)

pes_width = cd.shared.calculate_median(
    np.concatenate((df['lp_w'].values, df['rp_w'].values)),
    np.concatenate((df['lp_dw'].values, df['rp_dw'].values)),
    color_index=0,
    plot_name='Width'
)

pes_length = cd.shared.calculate_median(
    np.concatenate((df['lp_l'].values, df['rp_l'].values)),
    np.concatenate((df['lp_dl'].values, df['rp_dl'].values)),
    color_index=1,
    plot_name='Length'
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

manus_width = cd.shared.calculate_median(
    np.concatenate((df['lm_w'].values, df['rm_w'].values)),
    np.concatenate((df['lm_dw'].values, df['rm_dw'].values)),
    color_index=2,
    plot_name='Width'
)

manus_length = cd.shared.calculate_median(
    np.concatenate((df['lm_l'].values, df['rm_l'].values)),
    np.concatenate((df['lm_dl'].values, df['rm_dl'].values)),
    color_index=3,
    plot_name='Length'
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

pes_aspects = [
    l / w for l, w in zip(
        pes_length['measurements'],
        pes_width['measurements']
    )
]
pes_aspect = cd.shared.calculate_median(
    *mstats.values.unzip(pes_aspects),
    color_index=4,
    plot_name='Pes'
)

manus_aspects = [
    l / w for l, w in zip(
        manus_length['measurements'],
        manus_width['measurements']
    )
]
manus_aspect = cd.shared.calculate_median(
    *mstats.values.unzip(manus_aspects),
    color_index=5,
    plot_name='Manus'
)

cd.display.plotly(
    data=[
        pes_aspect['trace'],
        manus_aspect['trace']
    ],
    layout=plotting.create_layout(
        title='Aspects Ratios Manus: {} & Pes: {}'.format(
            manus_aspect['median'].html_label,
            pes_aspect['median'].html_label
        ),
        x_label='Aspect Ratio (#)',
        y_label='Probability Density (AU)'
    )
)

cd.shared.entire_trackway = dict(
    pes_aspect=pes_aspect,
    pes_width=pes_width,
    pes_length=pes_length,
    manus_aspect=manus_aspect,
    manus_width=manus_width,
    manus_length=manus_length
)
