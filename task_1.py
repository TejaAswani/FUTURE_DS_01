import streamlit as st
import pandas as pd
import plotly.express as px

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(page_title="Business Analytics Dashboard", layout="wide")
# ==============================
# DARK THEME CSS
# ==============================
st.markdown("""
    <style>
    body {
        background-color: #0e1117;
        color: white;
    }
    .card {
        padding: 20px;
        border-radius: 12px;
        color: white;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# ==============================
# LOAD DATA
# ==============================
df = pd.read_csv("superstore.csv")

# CLEAN DATA
df['Region'] = df['Region'].astype(str).str.strip()
df['Category'] = df['Category'].astype(str).str.strip()
df['Product Name'] = df['Product Name'].astype(str).str.strip()
df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
df = df.dropna()

# ==============================
# HEADER
# ==============================
st.markdown(
    "<h1 style='text-align:center; color:#1E90FF;'>📊 Business Analytics Dashboard</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center;'>Transforming data into actionable business insights</p>",
    unsafe_allow_html=True
)
# ==============================
# SIDEBAR
# ==============================
st.sidebar.header("🔍 Filters")

region = st.sidebar.selectbox("Select Region", sorted(df['Region'].unique()))
category_options = ["All"] + list(df['Category'].unique())
category = st.sidebar.selectbox("Select Category", category_options)

# FILTER LOGIC
if category == "All":
    filtered_df = df[df['Region'] == region]
else:
    filtered_df = df[(df['Region'] == region) & (df['Category'] == category)]

# ==============================
# MAIN CONTENT
# ==============================
if filtered_df.empty:
    st.warning("No data available")
else:
    # KPIs
    col1, col2 = st.columns(2)

    col1.markdown(f"""
        <div class="card" style="background: linear-gradient(135deg, #1f77b4, #00ADB5);">
        <h3>💰 Total Sales</h3>
        <h1>{filtered_df['Sales'].sum():,}</h1>
        </div>
    """, unsafe_allow_html=True)

    col2.markdown(f"""
        <div class="card" style="background: linear-gradient(135deg, #2ca02c, #00ff99);">
        <h3>📈 Total Profit</h3>
        <h1>{filtered_df['Profit'].sum():,}</h1>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("##")

    # CHARTS
    col3, col4 = st.columns(2)

    # Sales by Product
    with col3:
        st.subheader("📦 Top Products")

        product_sales = filtered_df.groupby('Product Name')['Sales'].sum().reset_index()
        product_sales = product_sales.sort_values(by='Sales', ascending=False).head(8)

        fig1 = px.bar(
            product_sales,
            x='Sales',
            y='Product Name',
            orientation='h',
            color='Sales',
            color_continuous_scale='Teal'
        )
        fig1.update_layout(template="plotly_dark")
        st.plotly_chart(fig1, use_container_width=True)

    # Donut Chart
    with col4:
        st.subheader("🥧 Category Contribution")

        category_profit = df.groupby('Category')['Profit'].sum().reset_index()

        fig2 = px.pie(
            category_profit,
            names='Category',
            values='Profit',
            hole=0.5
        )
        fig2.update_layout(template="plotly_dark")
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("##")

    # Sales Trend
    st.subheader("📅 Sales Trend")

    sales_trend = df.groupby('Order Date')['Sales'].sum().reset_index()

    fig3 = px.line(
    sales_trend,
    x='Order Date',
    y='Sales',
    markers=True,
    color_discrete_sequence=["#B50045"]
    )

    fig3.update_traces(line=dict(width=4))
    fig3.update_layout(
    template="plotly_dark",
    title="Sales Trend Over Time"
    )

    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("##")
     # ==============================
    # KEY INSIGHTS
    # ==============================
    st.markdown("## 📝 Key Insights & Recommendations")

    st.markdown("""
    - The business generated a total sales of {:,} with a profit of {:,}, indicating overall profitability.
    - The profit margin is healthy, showing efficient cost management and pricing strategy.
    - A few top-performing products contribute significantly to total revenue, suggesting a strong product focus.
    - The category contribution analysis shows that certain categories dominate sales, while others have lower impact.
    - The sales trend over time helps identify periods of growth and possible seasonal demand patterns.

    **Recommendations:**
    - Focus marketing efforts on top-performing products to maximize revenue.
    - Improve or rethink strategy for low-performing categories.
    - Analyze high-sales periods and replicate strategies to boost future performance.
    """.format(filtered_df['Sales'].sum(), filtered_df['Profit'].sum()))
    # DOWNLOAD BUTTON
    csv = filtered_df.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="📥 Download Filtered Data",
        data=csv,
        file_name='filtered_sales_data.csv',
        mime='text/csv'
    )

    # DATA TABLE
    st.subheader("📄 Data Preview")
    st.dataframe(filtered_df)