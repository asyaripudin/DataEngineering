import pandas as pd 
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# ==========================================
# 1. BACA FILE CSV (EXTRACT)
# ==========================================

data = pd.read_csv("../extract/annex2.csv", delimiter=";")
df=pd.DataFrame(data)
print("DataFrame:")
print(df)
#info about the data
print("DataFrame info:")
print(df.info())

# ==========================================
# 2. TRANSFORMATION
# ==========================================
# membersihkan nama column column
df.columns = df.columns.str.strip()

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
print(df['Date'].dtype)
df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')

df['Time'] = pd.to_datetime(
    df['Time'],
    format='%H:%M:%S.%f',
    errors='coerce'
)
print(df['Time'].dtype)
df['Time'] = df['Time'].dt.strftime('%H:%M:%S')

#df info
print("DataFrame Info Type data:")
print(df.info())
# tampilan data setelah transformasi
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

# ==========================================
# 3. LOAD (INSER KE SQL SERVER)
# ==========================================
connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost,1434;"
    "DATABASE=DataEngineering;"
    "UID=sa;"
    "PWD=Jakarta@202608;"
    "TrustServerCertificate=yes;"    
)
connection_url = "mssql+pyodbc:///?odbc_connect=" + quote_plus(
    connection_string
)
engine = create_engine(connection_url)
# input dataframe ke sql server
df.to_sql(
    "annex2",
    con=engine,
    if_exists="append",
    index=False
)