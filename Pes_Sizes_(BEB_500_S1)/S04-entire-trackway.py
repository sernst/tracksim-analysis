import cauldron as cd
import numpy as np

df = cd.shared.df

pes_length = cd.shared.calculate_median(
    np.concatenate((df['lp_l'].values, df['rp_l'].values)),
    np.concatenate((df['lp_dl'].values, df['rp_dl'].values))
)

pes_width = cd.shared.calculate_median(
    np.concatenate((df['lp_w'].values, df['rp_w'].values)),
    np.concatenate((df['lp_dw'].values, df['rp_dw'].values))
)

cd.display.markdown(
    """
    Entire Trackway
    ===============

    The following are the results for the entire trackway.

    * Pes Width: **{{ pes_width.html_label }} m**
    * Pes Length: **{{ pes_length.html_label }} m**
    """,
    pes_length=pes_length,
    pes_width=pes_width
)
