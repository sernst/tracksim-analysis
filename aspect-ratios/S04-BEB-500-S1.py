import cauldron as cd

df = cd.shared.df

df = df[
    (df['site'] == 'BEB') &
    (df['level'] == '500') &
    (df['number'] == '1')
]

cd.display.header('BEB 500 S1 Data')
cd.shared.process(df)
