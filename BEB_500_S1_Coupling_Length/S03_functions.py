import typing

import cauldron as cd
from cauldron import plotting
import pandas as pd
from plotly import graph_objs as go


def per_trial(
        data_frame: pd.DataFrame,
        function,
        **kwargs
):
    """
    Calls the specified function on each trial in the specified
    data frame. The signature for the function is:

        function(data_frame_row, trial_data, **kwargs)

    :param data_frame:
    :param function:
    :return:
        A dictionary containing the returned values of each function
        where the keys are the ID of the trial on which the function was
        executed.
    """

    results = dict()

    trial_kwargs = dict()
    for index, row in data_frame.iterrows():
        trial_id = row.id

        for key, value in kwargs.items():
            if key.startswith('_'):
                trial_kwargs[key[1:]] = value[trial_id]
            else:
                trial_kwargs[key] = value

        for t in cd.shared.trials:
            if t['id'] == trial_id:
                results[t['id']] = function(row, t, **trial_kwargs)

    return results

cd.shared.per_trial = per_trial


def create_scatter(
        data_frame: pd.DataFrame,
        value_column: typing.Union[str, list],
        uncertainty_column: typing.Union[str, list] = None,
        x_column: typing.Union[str, list] = None,
        sort_by: typing.Union[str, list] = 'separation'
):
    """
    Create a scatter plot for each row in the specified data frame where the
    x, y and y uncertainty values are defined by column names or a Series/list
    where the elements match the order of the entries in the data frame.

    :param data_frame:
    :param value_column:
    :param uncertainty_column:
    :param x_column:
    :param sort_by:
    :return:
    """

    traces = []
    data_frame = data_frame.copy()  # type: pd.DataFrame
    ids = data_frame.id.tolist()

    for index, gait_id in enumerate(sorted(data_frame.gait_id.unique())):
        df_slice = data_frame[data_frame.gait_id == gait_id]

        if sort_by:
            df_slice = df_slice.sort_values(by=sort_by)

        if isinstance(uncertainty_column, str):
            uncertainties = df_slice[uncertainty_column]
        elif uncertainty_column is None:
            uncertainties = None
        else:
            uncertainties = [
                uncertainty_column[ids.index(tid)]
                for tid in df_slice.id
                ]

        if isinstance(value_column, str):
            values = df_slice[value_column]
        else:
            values = [
                value_column[ids.index(tid)]
                for tid in df_slice.id
                ]

        if x_column is None:
            x = df_slice.order
        elif isinstance(x_column, str):
            x = df_slice[x_column]
        else:
            x = [
                x_column[ids.index(tid)]
                for tid in df_slice.id
                ]

        if uncertainty_column:
            error_y = {
                'type': 'data',
                'visible': True,
                'array': uncertainties
            }
        else:
            error_y = {
                'visible': False
            }

        traces.append(go.Scatter(
            x=x,
            y=values,
            error_y=error_y,
            mode='markers',
            marker={
                'size': 6,
                'color': plotting.get_color(index)
            },
            text=df_slice.short_id,
            name=gait_id
        ))

    return traces

cd.shared.create_scatter = create_scatter
