import pandas as pd
import numpy as np

data = pd.read_csv("../extract/annex2.csv", delimiter=";")
df=pd.DataFrame(data)
print("DataFrame:")
print(df)
#info about the data
print("DataFrame info:")
print(df.info())
#Cek Nilai kosong
print("Cek Nilai kosong:")
print(df.isna().sum())
# memeriksa data duplikat
print("Cek Data Duplikat:")
print(df.duplicated().sum())

# Menyesuaikan tipe data
df['Date'] = pd.to_datetime(
    df['Date'],
    format='%d/%m/%Y',
    errors='coerce'
)

df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')


df['Time'] = pd.to_datetime(
    df['Time'],
    format='%H:%M:%S.%f',
    errors='coerce'
)
df['Time'] = df['Time'].dt.strftime('%H:%M:%S')

#df info
print("DataFrame Info:")

print(df.info())

# tampilan data setelah transformasi
print("DataFrame:")
print(df)

# menambah kolom baru Revenue
df['Revenue'] = df['Quantity Sold (kilo)'] * df['Unit Selling Price (RMB/kg)']
print("DataFrame with Revenue:")
print(df.info())

# preview hasil

print("Preview Hasil Transformation:")
print(df[
    [
       'Date','Time','Item Code','Quantity Sold (kilo)', 'Unit Selling Price (RMB/kg)', 'Revenue','Sale or Return','Discount (Yes/No)'
    ]

].head())