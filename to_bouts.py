import pandas as pd
import numpy as np
from numpy.core.numeric import NaN

df = pd.DataFrame(pd.read_csv("001_chest_AX6_6014664.csv"))

df['key'] = (df['posture'] != df['posture'].shift(1)).astype(int).cumsum()
df = df.groupby(['key'], axis = 0, sort=False, as_index= False)['time', 'posture'].nth([0, -1]).reset_index()

df = pd.DataFrame({'sleep_start':df['time'].iloc[::].values, 'sleep_end':df['time'].iloc[::].values, 'posture':df['posture'].iloc[::].values})

df['matches?'] = df['posture'].shift(1)==df['posture']
df['matches2.0?'] = df['matches?'].shift(-1)==df['matches?']



df.loc[(df['matches2.0?'] == True), "matches2.0?"] = 2
df.loc[(df['matches2.0?'] == False), "matches2.0?"] = 1
df_new = pd.DataFrame([df.loc[idx] for idx in df.index for _ in range(df.loc[idx]['matches2.0?'])]).reset_index(drop=True)

df_new["bout_start"] = df_new["sleep_start"].iloc[::2]
df_new["bout_end"] = df_new["sleep_end"].iloc[1::2]
df_new = df_new.drop(columns = ["sleep_start", "sleep_end", "matches?", "matches2.0?"])

df_new['bout_end'] = df_new['bout_end'].shift(-1)
df_new = df_new.dropna().reset_index(drop = True)
df_new = df_new.reindex(columns=["bout_start", "bout_end", "posture"])
df_new

df_new.to_csv("test.csv", index=False)