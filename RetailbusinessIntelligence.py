import pandas as pd
from matplotlib import pyplot as plt

data = {
    "order_id":[101,102,103,104,105,106,107],
    "product_name":["Mouse","keyboard","Notebook","Pen","Monitor","Bag","Printer"],
    "category":["IT","IT","Stationery","Stationery","IT","Stationery","IT"],
    "quantity":[3,2,5,10,1,4,2],
    "price_each":[500,1200,50,10,7000,600,5000],
    "order_date":pd.to_datetime(
        ["2024-01-10","2024-01-12","2024-01-15","2024-01-20",
        "2024-02-01","2024-02-05","2024-02-10"]
    ),
    "region":["East","West","North","South","North","South","West"]
}

df = pd.DataFrame(data)
print(df)

# Export Raw Data to Excel
df.to_excel("sales_data.xlsx", index=False)
print("Raw sales data exported to sales_data.xlsx")


# Business Questions & Analysis
# 1.Total Sales Revenue
df["sales_amount"] =df["quantity"]*df["price_each"]
total_sales = df["sales_amount"].sum()

print("Total Sales Revenue:", total_sales)


# 2.Sales by Region
sales_by_region = df.groupby("region")["sales_amount"].sum().reset_index()
print("\nSales by Region:\n", sales_by_region)

#VISUALIZATION

plt.bar(sales_by_region["region"], sales_by_region["sales_amount"])
plt.title("Sales by Region")
plt.xlabel("Region")
plt.ylabel("Total Sales")
plt.show()

# 3.Top-Selling Products
top_products = df.groupby("product_name")["sales_amount"].sum().sort_values(ascending=False).head(3)
print("\nTop 3 Products:\n", top_products)

top_products.plot(kind="bar",title="Top 3 Products",ylabel="Sales")
plt.show()

# 4.Monthly Sales Trend
df["month"]=df["order_date"].dt.to_period("M")
monthly_sales = df.groupby("month")["sales_amount"].sum().reset_index()
print("\nMonthly Sales Trend:\n", monthly_sales)

monthly_sales.plot(x="month", y= "sales_amount", kind="line", marker="o", title="Monthly Sales Trend")
plt.show()

# Export All Reports To excel
with pd.ExcelWriter("sales_analysis.xlsx") as writer:
    df.to_excel(writer, sheet_name="Sheet1", index=False)
    sales_by_region.to_excel(writer, sheet_name="Sales by Region", index=False)
    top_products.to_excel(writer, sheet_name="Top Products")
    monthly_sales.to_excel(writer, sheet_name="Monthly Trend", index=False)

print("All reports exported to sales_analysis.xlsx")