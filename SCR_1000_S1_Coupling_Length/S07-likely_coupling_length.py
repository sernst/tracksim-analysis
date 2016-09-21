import cauldron as cd
import plotly.graph_objs as go
from cauldron import plotting
from tracksim import coupling

cd.refresh(coupling)

df = cd.shared.df
dist_data = coupling.distribution(df, 1.23, 2.1, 0.13)

distribution_trace = go.Scatter(
    x=dist_data['values']['x'],
    y=dist_data['values']['y'],
    name='Distribution',
    mode='lines',
    fill='tozeroy'
)

segment_trace = go.Scatter(
    x=dist_data['segment']['x'],
    y=dist_data['segment']['y'],
    mode='lines',
    name='Region',
    line=go.Line(
        color=plotting.get_color(1, 1.0),
        width=4
    )
)

gaussian_trace = go.Scatter(
    x=dist_data['gauss']['x'],
    y=dist_data['gauss']['y'],
    mode='lines',
    name='Region Fit',
    line=go.Line(
        color='rgba(0, 0, 0, 0.75)',
        dash='dash',
        width=3
    )
)

cd.display.plotly(
    [distribution_trace, segment_trace, gaussian_trace],
    layout=plotting.create_layout(
        title='Kernel Density Solution Fitness',
        x_label='Coupling Length (m)',
        y_label='Fitness Density (AU)'
    )
)

cd.display.markdown(
    """
    Estimate of the coupling length is: {{ cl }} m
    """,
    cl=dist_data['coupling_length'].html_label
)


