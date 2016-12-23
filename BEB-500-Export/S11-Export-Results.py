import re

import cauldron as cd
import pandas as pd

df_out = cd.shared.df_out  # type: pd.DataFrame
csv_columns = cd.shared.csv_columns  # type: list

filename = 'BEB-500 Catalog.csv'

# Skip the index column
column_names = [column.name for column in csv_columns[1:]]

df_export = df_out \
    .fillna('') \
    .drop(labels=['uid', 'index'], axis=1)  # type: pd.DataFrame

df_export.to_csv(filename, index=False, columns=column_names)

with open(filename, 'r') as fp:
    csv_contents = fp.read()

with open(filename, 'w') as fp:
    fp.write(re.sub(r'\.([1-9]+)0{2,}[0-9]+', r'.\1', csv_contents))

cd.display.markdown(
    """
    # Export Results

    A portion of the final results are printed in the table below for
    validation.
    """
)

cd.display.table(df_export.head(100))
