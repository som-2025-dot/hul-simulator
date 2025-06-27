# 🧴 HUL Price & Revenue Simulator

An interactive Streamlit web app that predicts the impact of price changes on:
- 🧾 Units sold
- 💰 Revenue (absolute & % change)
- ⚠️ Churn rate
- 📉 Market share

Built with real-world FMCG logic — combining price elasticity, brand loyalty, and competitive pressure.

---

## 🚀 Features

✅ Adjust product prices using sliders  
✅ Predict how price impacts unit sales using ML  
✅ Calculate revenue impact (₹ and %)  
✅ Estimate churn and its effect on market share  
✅ Visualize with colorful Plotly bar & pie charts  
✅ Fully interactive, mobile-friendly UI

---

## 📂 Files in this repo

| File                        | Purpose                              |
|----------------------------|--------------------------------------|
| `streamlit_app.py`         | Main Streamlit dashboard code        |
| `fmcg_predictive_model_dataset.csv` | Dataset used for training & simulation |
| `requirements.txt`         | Required Python packages for deploy  |

---

## 🛠 Tech Stack

- **Frontend:** Streamlit  
- **ML Model:** Scikit-learn (Linear Regression)  
- **Visualization:** Plotly  
- **Deployment:** Streamlit Cloud

---

## 📈 Demo

👉 [Live App on Streamlit](https://YOUR-APP-URL.streamlit.app) *(replace after deployment)*

---

## 📦 Installation (Local)

```bash
git clone https://github.com/YOUR_USERNAME/hul-simulator.git
cd hul-simulator
pip install -r requirements.txt
streamlit run streamlit_app.py
