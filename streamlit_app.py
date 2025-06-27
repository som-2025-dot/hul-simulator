import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import plotly.express as px

# --- Load Data ---
df = pd.read_csv("fmcg_predictive_model_dataset.csv")

# One-hot encode category
df_encoded = pd.get_dummies(df, columns=['Category'], drop_first=True)

# Define features
feature_cols = ['Base Price', 'Brand Loyalty', 'Market Share (%)', 'Elasticity'] + \
               [col for col in df_encoded.columns if col.startswith("Category_")]

# Model Training
X = df_encoded[feature_cols]
y = df_encoded['Base Units Sold']
model = LinearRegression()
model.fit(X, y)

# --- Streamlit UI ---
st.set_page_config(page_title="HUL Price Simulator", layout="wide")
st.title("🧴 HUL Price & Revenue Simulator")

# Product Selection
product_name = st.selectbox("Select a Product", df['Product Name'].unique())
product_row = df[df['Product Name'] == product_name].sample(1).squeeze()

# Display Base Info
st.markdown(f"**Category:** {product_row['Category']}  \n"
            f"**Base Price:** ₹{product_row['Base Price']}  \n"
            f"**Base Units Sold:** {product_row['Base Units Sold']}  \n"
            f"**Elasticity:** {product_row['Elasticity']}  \n"
            f"**Brand Loyalty:** {product_row['Brand Loyalty']}  \n"
            f"**Market Share:** {product_row['Market Share (%)']}%")

# Slider to change price (wide range)
new_price = st.slider(
    "Adjust New Price (₹)",
    min_value=20.0,
    max_value=400.0,
    value=round(product_row['Base Price'], 2),
    step=0.5
)

# --- Prediction Logic ---
input_data = {
    'Base Price': new_price,
    'Brand Loyalty': product_row['Brand Loyalty'],
    'Market Share (%)': product_row['Market Share (%)'],
    'Elasticity': product_row['Elasticity']
}

# One-hot encode the category input
for col in [col for col in X.columns if col.startswith("Category_")]:
    input_data[col] = 1 if col == f"Category_{product_row['Category']}" else 0

input_df = pd.DataFrame([input_data])
predicted_units = int(model.predict(input_df)[0])

# Revenue calculations
original_revenue = product_row['Base Price'] * product_row['Base Units Sold']
new_revenue = new_price * predicted_units
revenue_change = new_revenue - original_revenue
revenue_pct_change = (revenue_change / original_revenue) * 100

# --- Churn logic (competitive) ---
competitor_price = product_row['Base Price'] * 0.9
price_gap_vs_competitor = (new_price - competitor_price) / competitor_price

# New churn formula
churn_rate = max(0, price_gap_vs_competitor * 100 *
                 (1 - product_row['Brand Loyalty']) *
                 (1 + abs(product_row['Elasticity'])))

# Market Share Adjustment
new_market_share = max(0, product_row['Market Share (%)'] -
                          (churn_rate * product_row['Market Share (%)'] / 100))

# --- Display KPIs ---
st.subheader("📊 Simulation Results")

col1, col2, col3 = st.columns(3)
col1.metric("📦 Units Sold", f"{predicted_units:,}",
            delta=f"{predicted_units - product_row['Base Units Sold']:,}")
col2.metric("💰 Revenue", f"₹{new_revenue:,.2f}",
            delta=f"{revenue_pct_change:.2f}%")
col3.metric("⚠️ Churn Rate", f"{churn_rate:.2f}%")

st.metric("📉 Market Share", f"{new_market_share:.2f}%",
          delta=f"{new_market_share - product_row['Market Share (%)']:.2f}%")

# --- Visuals: Enhanced Charts ---
rev_df = pd.DataFrame({
    "Stage": ["Original", "Simulated"],
    "Revenue": [original_revenue, new_revenue]
})
st.plotly_chart(
    px.bar(
        rev_df,
        x="Stage",
        y="Revenue",
        text_auto=True,
        color="Stage",
        color_discrete_map={"Original": "#636EFA", "Simulated": "#EF553B"},
        title="💰 Revenue Comparison",
        template="plotly_dark"
    ).update_layout(showlegend=False)
)

market_df = pd.DataFrame({
    "Company": ["HUL", "Competitors"],
    "Market Share": [new_market_share, 100 - new_market_share]
})
st.plotly_chart(
    px.pie(
        market_df,
        names="Company",
        values="Market Share",
        hole=0.4,
        color="Company",
        color_discrete_map={"HUL": "#00CC96", "Competitors": "#AB63FA"},
        title="📊 Updated Market Share"
    ).update_traces(textinfo='percent+label')
)
