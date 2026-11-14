
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Retail Business Intelligence", page_icon="📊", layout="wide")

st.title("📊 Retail Business Intelligence Dashboard")
st.write("Retail Sales Data Analysis using Python, Pandas and Data Visualization")

data = {
    "order_id": [101, 102, 103, 104, 105, 106, 107],
    "product_name": ["Mouse", "Keyboard", "Notebook", "Pen", "Monitor", "Bag", "Printer"],
    "category": ["IT", "IT", "Stationery", "Stationery", "IT", "Stationery", "IT"],
    "quantity": [3, 2, 5, 10, 1, 4, 2],
    "price_each": [500, 1200, 50, 10, 7000, 600, 5000],
    "order_date": pd.to_datetime([
        "2024-01-10", "2024-01-12", "2024-01-15",
        "2024-01-20", "2024-02-01", "2024-02-05", "2024-02-10"
    ]),
    "region": ["East", "West", "North", "South", "North", "South", "West"]
}

df = pd.DataFrame(data)
df["sales_amount"] = df["quantity"] * df["price_each"]

st.subheader("Sales Overview")
c1, c2, c3 = st.columns(3)
c1.metric("Total Revenue", f"₹{df['sales_amount'].sum():,}")
c2.metric("Total Orders", len(df))
c3.metric("Products", df["product_name"].nunique())

st.divider()

st.subheader("Sales Dataset")
st.dataframe(df, use_container_width=True)

st.subheader("Sales by Region")
st.bar_chart(df.groupby("region")["sales_amount"].sum())

st.subheader("Top 3 Products")
top_products = df.groupby("product_name")["sales_amount"].sum().nlargest(3)
st.bar_chart(top_products)

st.subheader("Monthly Sales Trend")
df["month"] = df["order_date"].dt.strftime("%Y-%m")
monthly_sales = df.groupby("month")["sales_amount"].sum()
st.line_chart(monthly_sales)

st.subheader("Download Sales Report")
st.download_button(
    "Download CSV Report",
    df.to_csv(index=False).encode("utf-8"),
    "sales_analysis.csv",
    "text/csv"
)
