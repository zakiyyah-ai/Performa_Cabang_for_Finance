# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
#import package pandas
import pandas as pd
import numpy as np


# %%
#membaca data loan disbursement
df_loan = pd.read_csv('https://storage.googleapis.com/dqlab-dataset/loan_disbursement.csv')
df_loan


# %%
df_loan.info()


# %%
#mengubah type tanggal_cair ke dalam datetime
df_loan['tanggal_cair'] = pd.to_datetime(df_loan['tanggal_cair'])


# %%
df_loan.info()


# %%
#Memfilter data bulan Mei 2020, dan jumlahkan data per cabang
df_loan_amount = df_loan[(df_loan['tanggal_cair'] >= '2020-05-01') & (df_loan['tanggal_cair'] <= '2020-05-31')].groupby('cabang').sum()
df_loan_amount


# %%
#Tampilkan data 5 cabang dengan total amount paling besar
df_loan_terbesar = df_loan_amount.sort_values('amount', ascending=False).head()
df_loan_terbesar


# %%
#Tampilkan data 5 cabang dengan total amount paling kecil
df_loan_terkecil = df_loan_amount.sort_values('amount', ascending=True).head()
df_loan_terkecil


# %%
#Menghitung umur cabang (dalam bulan)
#Gabungkan data umur dan performa mei
df_loan_amount['pertama_cair'] = df_loan.tanggal_cair.groupby(df_loan['cabang']).min()
df_loan_amount['umur'] = (pd.to_datetime('2020-05-15').month) - (df_loan_amount['pertama_cair'].dt.month)
df_loan_amount


# %%
df_loan_amount.to_csv('C:\\Users\\User\\Downloads\\DATASET-DATASCIENCE-20211015T124508Z-001\\performa cabang\\df_loan_amount.csv')


# %%
df_loan_amount.info()


# %%
df_quantile = df_loan_amount.copy()
df_quantile


# %%
df = df_quantile[['umur','amount']].groupby(df_quantile['umur']).quantile(.25)
df['umur'] = df['umur'].astype(int)
df['Q3']= df_quantile[['amount']].groupby(df_quantile['umur']).quantile(.75)
df['Q3'] = df['Q3'].astype(int)
df = df.rename({'amount': 'Q1'}, axis=1)
df['IQR'] = df['Q3'] - df['Q1']
df['Q1-IQR'] = df['Q1'] - df['IQR']
df


# %%
df_loan_flag = pd.merge(

    df_loan_amount, df, left_on="umur", right_index=True, how="left", sort=False

)
df_loan_flag


# %%
del df_loan_flag['umur_y']
df_loan_flag = df_loan_flag.rename({'umur_x': 'umur'}, axis=1)
df_loan_flag


# %%
df_loan_flag.loc[df_loan_flag['amount'] < df_loan_flag['Q1-IQR'], 'flag'] = 'Rendah'
df_loan_flag.loc[df_loan_flag['amount'] > df_loan_flag['Q1-IQR'], 'flag'] = 'Baik'
df_loan_flag


# %%
df_loan_flag.to_csv('C:\\Users\\User\\Downloads\\DATASET-DATASCIENCE-20211015T124508Z-001\\performa cabang\\df_loan_flag.csv')


# %%
df_loan_mei = df_loan_flag[df_loan_flag['umur'] == 3]
df_loan_mei


# %%



