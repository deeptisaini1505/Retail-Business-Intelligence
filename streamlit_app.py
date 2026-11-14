
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Retail Business Intelligence",
    page_icon="📊",
    layout="wide"
)

# Custom styling
st.markdown("""
<style>
.stApp {
    background-color: #f4f7fb;
}
[data-testid="stMetric"] {
    background: white;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #e1e8f0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
[data-testid="stSidebar"] {
    background-color: #10243a;
}
[data-testid="stSidebar"] * {
    color: white !important;
}
h1, h2, h3 {
    color: #10243a;
}
</style>
""", unsafe_allow_html=True)

# Load actual Excel dataset
file_path = Path("sales_analysis.xlsx")

st.title("📊 Retail Business Intelligence")
st.caption("Retail Sales Performance | Python • Pandas • Streamlit • Plotly")

if not file_path.exists():
    st.error("sales_data.xlsx not found. Please check that the Excel file is in the repository root.")
    st.stop()

df = pd.read_excel(file_path)
df.columns = df.columns.str.strip().str.lower()

required = [
    "order_id", "product_name", "category", "quantity",
    "price_each", "order_date", "region", "sales_amount"
]

missing = [col for col in required if col not in df.columns]

if missing:
    st.error(f"Missing columns in Excel file: {', '.join(missing)}")
    st.stop()

df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
df["sales_amount"] = pd.to_numeric(df["sales_amount"], errors="coerce")
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
df = df.dropna(subset=["order_date", "sales_amount", "quantity"])

# Sidebar filters
st.sidebar.title("Dashboard Filters")

regions = sorted(df["region"].dropna().unique())
categories = sorted(df["category"].dropna().unique())

selected_regions = st.sidebar.multiselect(
    "Select Region", regions, default=regions
)

selected_categories = st.sidebar.multiselect(
    "Select Category", categories, default=categories
)

filtered = df[
    df["region"].isin(selected_regions)
    & df["category"].isin(selected_categories)
].copy()

st.sidebar.divider()
st.sidebar.caption(f"Dataset contains {len(df)} orders.")

if filtered.empty:
    st.warning("No records match the selected filters.")
    st.stop()

# KPI calculations
revenue = filtered["sales_amount"].sum()
orders = filtered["order_id"].nunique()
units = filtered["quantity"].sum()
avg_order = revenue / orders if orders else 0

st.subheader("Business Overview")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Revenue", f"₹{revenue:,.0f}")
c2.metric("Total Orders", f"{orders:,}")
c3.metric("Units Sold", f"{units:,.0f}")
c4.metric("Average Order Value", f"₹{avg_order:,.0f}")

st.divider()

# Monthly sales trend
st.subheader("📈 Monthly Revenue Trend")

monthly = (
    filtered.assign(month=filtered["order_date"].dt.to_period("M").astype(str))
    .groupby("month", as_index=False)["sales_amount"].sum()
)

fig_month = px.line(
    monthly,
    x="month",
    y="sales_amount",
    markers=True,
    text="sales_amount",
    labels={"month": "Month", "sales_amount": "Revenue (₹)"},
    template="plotly_white"
)
fig_month.update_traces(line_color="#2878B5", line_width=3)
fig_month.update_layout(
    margin=dict(l=10, r=10, t=25, b=10),
    height=350
)
st.plotly_chart(fig_month, use_container_width=True)

# Region and category charts
left, right = st.columns(2)

with left:
    st.subheader("🌍 Revenue by Region")
    region_sales = (
        filtered.groupby("region", as_index=False)["sales_amount"].sum()
        .sort_values("sales_amount", ascending=False)
    )
    fig_region = px.bar(
        region_sales,
        x="region",
        y="sales_amount",
        color="region",
        labels={"region": "Region", "sales_amount": "Revenue (₹)"},
        template="plotly_white"
    )
    fig_region.update_layout(showlegend=False, height=350)
    st.plotly_chart(fig_region, use_container_width=True)

with right:
    st.subheader("📦 Category-wise Sales")
    category_sales = (
        filtered.groupby("category", as_index=False)["sales_amount"].sum()
    )
    fig_category = px.pie(
        category_sales,
        names="category",
        values="sales_amount",
        hole=0.55,
        template="plotly_white"
    )
    fig_category.update_layout(height=350)
    st.plotly_chart(fig_category, use_container_width=True)

# Top products
st.subheader("🏆 Top Products by Revenue")

top_products = (
    filtered.groupby("product_name", as_index=False)["sales_amount"]
    .sum()
    .sort_values("sales_amount", ascending=False)
    .head(5)
)

fig_products = px.bar(
    top_products,
    x="sales_amount",
    y="product_name",
    orientation="h",
    text="sales_amount",
    labels={"sales_amount": "Revenue (₹)", "product_name": "Product"},
    template="plotly_white"
)
fig_products.update_layout(
    yaxis={"categoryorder": "total ascending"},
    height=350
)
st.plotly_chart(fig_products, use_container_width=True)

# Detailed data
st.subheader("📋 Sales Details")
st.dataframe(filtered, use_container_width=True, hide_index=True)

# Download report
st.download_button(
    label="⬇️ Download Filtered Sales Report",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name="retail_sales_report.csv",
    mime="text/csv"
)

st.caption(
    "Retail Business Intelligence Dashboard | "
    "Data source: sales_data.xlsx | Profit is not calculated because cost data is unavailable."
)

