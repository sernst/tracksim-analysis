import cauldron as cd
import plotly.graph_objs as go

tracks_df = cd.shared.tracks_df

cd.display.plotly(
    go.Histogram(
        x=tracks_df['dw']
    ),
    {}
)

cd.display.plotly(
    go.Histogram(
        x=tracks_df['dw'] / tracks_df['w']
    ),
    {}
)
