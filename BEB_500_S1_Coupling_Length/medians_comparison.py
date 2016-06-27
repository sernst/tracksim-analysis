import pandas as pd
import cauldron as cd
from cauldron import plotting
import plotly.graph_objs as go

df = cd.shared.df  # type: pd.DataFrame

df['variance'] = 100.0 * df.uncertainty / df.coupling_length

traces = []

for index, gait_id in enumerate(sorted(df.gait_id.unique())):
    df_slice = df[df.gait_id == gait_id]
    df_slice = df_slice.sort_values(by='separation')

    traces.append(go.Scatter(
        x=df_slice.order,
        y=df_slice.coupling_length,
        error_y={
            'visible': True,
            'value': df_slice.uncertainty
        },
        mode='markers',
        marker={
            'size': 6,
            'color': plotting.get_color(index, 0.7)
        },
        text=df_slice.id,
        name=gait_id
    ))

cd.display.header('Median Coupling Lengths')

cd.display.plotly(
    data=traces,
    layout=plotting.create_layout(
        {'hovermode': 'closest'},
        title='Median Coupling Lengths by Trial',
        x_label='Trial Index (#)',
        y_label='Coupling Length (m)'
    )
)

cd.display.markdown(
    """
    There is a trend in the data of the uncertainties increasing as the median
    coupling length increases. This could indicate that the "better" solutions
    are the shorter ones due to their apparent less uncertain values. It could
    also be that this is a scaling issue, where the higher coupling length
    trials have a similar or less uncertainty proportionally than the shorter
    trials. Normalizing the uncertainties by coupling lengths yields a relative
    uncertainties value that will resolve this issue.
    """
)

colors = [plotting.get_color(int(tid[1])) for tid in df.id]

cd.display.plotly(
    data=go.Bar(
        y=df.variance,
        text=df.gait_id,
        marker=dict(
            color=colors
        )
    ),
    layout=plotting.create_layout(
        title='Relative Coupling Length Uncertainties',
        x_label='Trial Index (#)',
        y_label='Relative Uncertainty (%)'
    )
)


cd.display.markdown(
    """
    The relative uncertainties actually decrease as the coupling length
    increases. The trials with longer coupling lengths are proportionally less
    uncertain than the shorter ones. The trend in the previous plot was indeed
    a scaling artifact, and this suggests the longer coupling length trials
    are actually "better" solutions.

    _Note: It would be interesting to run these trials on even larger gaits to
    see if the trend continues, or if there is some other trend that appears
    in a larger separation, even if it's unlikely that those longer
    coupling-length gaits are physically reasonable solutions._

    The problem with this kind of statistical analysis is that it quantifies
    global trends in the data, not transient ones. While this can be very useful
    in reductive categorization analyses, this is not helpful in an analysis
    where global trends represent the noise and transient ones the signal. For
    example, what if one of the "better" solutions was regular for most of
    the simulation but with a brief period where the data was quite different.
    This type of statistical analysis would emphasize the more common, regular
    portion of the simulation and minimize the period where the data was
    different.

    To determine the "best" solution or solutions for the given data, we should
    be using an analysis that does not wash out the transient signals.
    """
)
