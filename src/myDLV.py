import numpy as np
import pandas as pd
# %matplotlib inline
from matplotlib import pyplot as plt
import os
import sys

def get_scrip_date(timestamp_lst):
  timestamp_lst2 = []
  #print(timestamp_lst[:5], type(timestamp_lst[0]))
  #print('-----------------------X--------X------------------')
  for timestmp in timestamp_lst:
    #print(timestmp, type(timestmp))
    timestmp_date = str(timestmp).split(' ', 1)
    #print('Timestamp', timestmp_date)
    timestamp_lst2.append(timestmp_date[0])
  print('Length of timestamp2', len(timestamp_lst2))
  return timestamp_lst2

directory_txt = os.fsencode('./data/txt/')
DF_list = list()
spxw_call_data = 0;

for file in os.listdir(directory_txt):
  filename = os.fsdecode(file)
  if filename.endswith(".txt"):
    date = filename[-14:-4]
    print(date)
    data = pd.read_csv('./data/txt/' + filename, sep="\t")
    EQT = pd.DataFrame(data)
    print(EQT.columns)
    # Import and Create Fields
    df = EQT[['okey_tk', 
              'okey_yr', 'okey_mn', 'okey_dy', 
              'okey_xx', 
              'okey_cp', 
              'prtSize', 'prtPrice',
              'prtIv', 
              'prtGa', 'prtTh', 'surfOpx', 'timestamp']]              
    df['okey_ymd'] = pd.to_datetime(df.loc[:, 'okey_yr'].astype(str) + '/' + df.loc[:, 'okey_mn'].astype(str) + '/' + df.loc[:, 'okey_dy'].astype(str))
    #print(df[['okey_yr', 'okey_mn', 'okey_dy', 'okey_ymd']])
    timestmp_lst = df.loc[:, ('timestamp')].tolist()
    #print(type(timestmp_lst))
    print(len(df['okey_ymd']))
    df['timestamp2'] = get_scrip_date(timestmp_lst)
    df['timestamp2'] = pd.to_datetime(df.loc[:, 'timestamp2'].astype(str))
    #print(df['timestamp2'].head())
    
    df['okey_maturity'] = df.loc[:, 'okey_ymd'] - df.loc[:, 'timestamp2']
    #print(df['okey_maturity'][13:20])
    df['okey_maturity'] = df.loc[:, 'okey_maturity'].dt.days
    #print(df['okey_maturity'][13:20])
    #df = df.drop_duplicates().sort_values(by=['okey_maturity'])

    print(df['okey_tk'].value_counts())
    #print(df.loc[df['okey_xx'] != 0, ['okey_tk', 'okey_ymd', 'okey_maturity', 'okey_xx', 'prtSize', 'prtPrice']])
    #print(df)
    print(len(df.loc[(df['prtPrice'] != 0) & (df['prtGa'] != 0) & (df['prtTh'] != 0) & (df['surfOpx'] != 0)]))
    #print(df[14:18])
    #df.reset_index(drop=True)
    #print(df[14:18])
    drp_lst = []
    for i in range(0, len(df)):
      a_string =  df.loc[i, 'okey_tk']
      #print(a_string)
      if a_string.startswith('E'):
        #print(df.loc[i, 'okey_tk'])
        #e_tk = e_tk.append(df.iloc[i], ignore_index=True)
        print('Done', i)
      else:
        drp_lst.append(i)
        #print('Not Done', i)

    df.drop(index=drp_lst, axis=0, inplace=True)
    df = df.loc[(df['prtPrice'] != 0) & (df['prtGa'] != 0) & (df['prtTh'] != 0) & (df['surfOpx'] != 0)]
    print('DF Length', len(df.loc[df['okey_cp'] == 'Call']))
    # SPX Weekly Call 
    #ew1 = df.loc[(df['okey_tk'] == 'EW3')]
    #print(len(ew1))
    #print(ew1['okey_maturity'].value_counts())
    #print(ew1.loc[ew1['okey_maturity'] == 77].columns)
    df_call = df.loc[(df['okey_cp'] == 'Call')]
    df_call = df_call[['okey_xx',  
              'okey_maturity',
              'prtSize', 'prtPrice',
              'prtIv', 
              'prtGa', 'prtTh', 'surfOpx']]
    #print(ew1_call)
    grouped_df = df_call.groupby(['okey_maturity', 'okey_xx'])
    spxw_call_clean = grouped_df.mean().reset_index() 
    spxw_call_data += spxw_call_clean.shape[0]
    print(len(spxw_call_clean), spxw_call_clean['okey_maturity'].value_counts())
    #print(spxw_call_clean.loc[spxw_call_clean['okey_xx'] != 0])
    plt.scatter(spxw_call_clean['okey_xx'], spxw_call_clean['okey_maturity'])
    plt.xlabel('option strike')
    plt.ylabel('date')
    DF_list.append(spxw_call_clean)
plt.show()