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

#menghapus baris yang tidak punya tanggal, quantity dan harga
df = df.dropna(
    subset=['Date', 'Time', 'Quantity Sold (kilo)', 'Unit Selling Price (RMB/kg)']
)

# tampilan data setelah transformasi
print("DataFrame:")
print(df)

# menambah kolom  Revenue
df['Revenue'] = df['Quantity Sold (kilo)'] * df['Unit Selling Price (RMB/kg)']
print("DataFrame with Revenue:")


# menambah kolom Bulan
df['Month'] = pd.to_datetime(df['Date']).dt.to_period('M').astype(str)

print(df.info())

# preview hasil

print("Preview Hasil Transformation:")
print(df[
    [
       'Date','Time','Item Code','Quantity Sold (kilo)', 'Unit Selling Price (RMB/kg)', 'Revenue','Month',
       'Sale or Return','Discount (Yes/No)'
    ]

].head())

# membuat agregasi
Total_Revenue = df['Revenue'].sum()
print("Total Revenue:")
print(Total_Revenue)

#revenue per bulan
Revenue_Per_Month = (df.groupby('Month', as_index = False).agg(Total_Revenue=("Revenue", "sum")))
print("Revenue per Month:")
print(Revenue_Per_Month)

# Top 5 Total_Revenue terbesar
Top_5_Revenue_Per_Month = (
    Revenue_Per_Month
    .sort_values('Total_Revenue', ascending=False)
    .head(5)
)

print("Top 5 Revenue per Month:")
print(Top_5_Revenue_Per_Month)

#revenue per item code
Revenue_Per_Item_Code = (df.groupby('Item Code', as_index = False).agg(Total_Revenue=("Revenue", "sum")))
print("Revenue per Item Code:")
print(Revenue_Per_Item_Code)

# Top 5 Revenue per Item Code
Top_5_Revenue_Per_Item_Code = (
    Revenue_Per_Item_Code
    .sort_values('Total_Revenue', ascending=False)
    .head(5)
)
print("Top 5 Revenue per Item Code:")
print(Top_5_Revenue_Per_Item_Code)

# membuat grafik
import matplotlib.pyplot as plt
fig, axes = plt.subplots(2,2, figsize = (15,10))
# Judul dasbor
fig.suptitle('Sales Dashboard', fontsize = 20)
# Memunculkan grafik
# chart 1 - Revenue per kota
axes[0,0].bar(
    Revenue_Per_Month['Month'],
    Revenue_Per_Month['Total_Revenue']
)
axes[0,0].set_title('Total Revenue per Month')
axes[0,0].set_xlabel('Month')
axes[0,0].set_ylabel('Total Revenue')
axes[0,0].tick_params(axis = "x", rotation = 45)

# chart 2 - revenue per item code
axes[0,1].plot(
    Revenue_Per_Item_Code['Item Code'],
    Revenue_Per_Item_Code['Total_Revenue'],
    marker='o'
)
axes[0,1].set_title('Total Revenue per item Code')
axes[0,1].set_xlabel('Item Code')
axes[0,1].set_ylabel('Total Revenue')
axes[0,1].tick_params(axis = "x", rotation = 45)
axes[1, 0].grid(axis="y", alpha=0.3)

# chart 3 - Top 5 Revenue per Month

chart_data = Top_5_Revenue_Per_Month.iloc[::-1]
axes[1,0].barh(
    chart_data['Month'],
    chart_data['Total_Revenue']
)
axes[1,0].set_title('Top 5 Revenue per Month')
axes[1,0].set_xlabel('Total Revenue')
axes[1,0].set_ylabel('Month')

# chart 4 - Top 5 Revenue per Item Code
chart_data = Top_5_Revenue_Per_Item_Code.iloc[::-1]
axes[1,1].barh(
    chart_data['Item Code'],
    chart_data['Total_Revenue']
)
axes[1,1].set_title('Top 5 Revenue per Item Code')
axes[1,1].set_xlabel('Total Revenue')
axes[1,1].set_ylabel('Item Code')

plt.tight_layout()
plt.show()