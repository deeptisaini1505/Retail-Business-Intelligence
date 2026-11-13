import pandas as pd
import matplotlib.pyplot as plt

data = {
    'Product':['Laptop','Tablet','Laptop','Monitor','Tablet','Monitor'],
    'Region':['East','West','North','East','West','North'],
    'Units_Sold':[100,150,200,80,90,120],
    'Unit_Price':[800,300,850,200,310,210]
}

df=pd.DataFrame(data)
pd.set_option('display.max_columns', None)

#Calculate Total Revenue
df['Revenue']= df['Units_Sold']*df['Unit_Price']

print("Full Dataset:")
print(df)

#Conditional Filtering
#python
#copy
#edit

#Example: Filter products with revenue over 20,000
high_revenue = df[df['Revenue'] > 20000]

print("\nProducts with Revenue > 20000:")
print(high_revenue)

#Group and Summarize
#python
#copy
#edit
#Total Revenue by product
product_revenue = df.groupby('Product')['Revenue'].sum().reset_index()

print("\nTotal Revenue by Product:")
print(product_revenue)

#Visualization using Matplotlib
#python
#copy
#edit
#Bar chart of revenue by product
plt.figure(figsize=(8,6))
plt.bar(product_revenue['Product'], product_revenue['Revenue'],color='skyblue')
plt.title('Total Revenue by Product')
plt.xlabel('Product')
plt.ylabel('Revenue($)')
plt.grid(axis='y')
plt.tight_layout()
plt.show()

#Bonus Conditional Highlight
#Add a flag if a product has high average unit price:
#python
#copy
#edit
#Add 'High Price' flag where average unit price > 500
df['High Price']= df['Unit_Price'].apply(lambda x: 'Yes' if x > 500 else 'No')
print("\nDataset with High Price")
