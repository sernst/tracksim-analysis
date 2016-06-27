import cauldron as cd
import pandas as pd


def per_trial(
        data_frame: pd.DataFrame,
        function
):
    """
    Calls the specified function on each trial in the specified
    data frame. The signature for the function is:

        function(trial_data)

    :param data_frame:
    :param function:
    :return:
        A dictionary containing the returned values of each function
        where the keys are the ID of the trial the function was executed
        upon.
    """

    results = dict()

    for trial_id in data_frame.id:
        for t in cd.shared.group['trials']:
            if t['id'] == trial_id:
                results[t['id']] = function(t)

    return results

cd.shared.per_trial = per_trial

