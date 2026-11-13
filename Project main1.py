import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt

df = pd.read_csv(r"C:\Users\DEEPTI SAINI\OneDrive\Desktop\Sales_data.csv")
pd.set_option('display.max_columns', None)
print(df)

# DATA PREPROCESSING
df.dropna(inplace=True)
df['Order Date'] = pd.to_datetime(df['ORDER DATE'])
df['Month'] = df['Order Date'].dt.month
df['sales'] = df['QUANTITY ORDERED'] * df['PRICE EACH']


sales_targets ={
    'USB-C CHARGING':2000,
    'BOSE SOUNDSPORT':1500,
    'GOOGLE PHONE':5000,
    'MACBOOK PRO LAPTOP':8000,
    'AAA BATTERIES(4-PACK)':1000,
    'WIRED HEADPHONE':1500
}
product_sales = df.groupby('PRODUCT')['sales'].sum().reset_index()
product_sales['Target'] = product_sales['PRODUCT'].map(sales_targets)
product_sales['Performance']=product_sales['sales'] - product_sales['Target']

plt.figure(figsize=(6,4))
plt.bar(product_sales['PRODUCT'], product_sales['sales'],label='Actual sales',color='r')
plt.bar(product_sales['PRODUCT'],product_sales['Target'],label='Target sales',alpha=0.5)
plt.xlabel('Product')
plt.ylabel('sales')
plt.title('Actual vs Target Sales by Product')
plt.legend()
plt.show()