import cauldron as cd
import plotly.graph_objs as go
from cauldron import plotting
import measurement_stats as mstats

df = cd.shared.couplings_df

variations = df['raw_mad'] / df['raw_median']

cd.display.plotly(
    data=go.Histogram(
        x=variations
    ),
    layout=plotting.create_layout(
        title='Coupling Length Fractional Deviations',
        x_label='Fractional Deviation',
        y_label='Frequency (#)'
    )
)

dist = mstats.create_distribution(
    measurements=variations.tolist(),
    uncertainties=0.01
)

x = mstats.distributions.uniform_range(dist, 3)
y = dist.probabilities_at(x)


cd.display.plotly(
    data=go.Scatter(
        x=x,
        y=y,
        mode='lines',
        fill='tozeroy'
    ),
    layout=plotting.create_layout(
        title='Coupling Length KDE',
        x_label='Coupling Lengths (m)',
        y_label='Expectation Value'
    )
)

