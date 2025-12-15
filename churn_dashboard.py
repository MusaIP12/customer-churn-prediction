import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from xgboost import plot_importance

# Set page config
st.set_page_config(page_title="Customer Churn Dashboard", layout="centered")

# Load data and model
df = pd.read_csv(r"Customer_Churn_Project/churn_dashboard_data.csv")
xgb2 = joblib.load(r"Customer_Churn_Project/xgb_model.pkl")

# Set custom contrasting colors
sns.set_style("whitegrid")
custom_colors = ["#1f77b4", "#ff7f0e"]  # Blue and orange

# Sidebar Filters
st.sidebar.header("🔎 Filter Data")
selected_gender = st.sidebar.selectbox("Filter by Gender", ["All", "Male", "Female"])
selected_geography = st.sidebar.selectbox("Filter by Geography", ["All"] + sorted(df['Geography'].unique()))

filtered_df = df.copy()
if selected_gender != "All":
    filtered_df = filtered_df[filtered_df["Gender"] == selected_gender]
if selected_geography != "All":
    filtered_df = filtered_df[filtered_df["Geography"] == selected_geography]

# Title
st.title("💼 Customer Churn Dashboard")

# Churn Overview
st.header("📊 Churn Distribution")
churn_counts = filtered_df['Exited'].value_counts().rename({0: 'Stayed', 1: 'Churned'})
fig1, ax1 = plt.subplots()
sns.barplot(x=churn_counts.index, y=churn_counts.values, ax=ax1, palette=custom_colors)
ax1.set_ylabel("Number of Customers")
st.pyplot(fig1)

# Churn by Geography
if 'Geography' in filtered_df.columns:
    st.header("🌍 Churn Rate by Geography")
    geo_churn = filtered_df.groupby('Geography')['Exited'].mean().sort_values(ascending=False)
    fig2, ax2 = plt.subplots()
    sns.barplot(x=geo_churn.index, y=geo_churn.values, ax=ax2, palette=custom_colors)
    ax2.set_ylabel("Churn Rate")
    st.pyplot(fig2)

# Churn by Age Group
if 'AgeGroup_Adult' in filtered_df.columns or 'AgeGroup_Senior' in filtered_df.columns:
    st.header("👥 Churn Rate by Age Group")

    def resolve_age_group(row):
        if row.get('AgeGroup_Senior', False):
            return 'Senior'
        elif row.get('AgeGroup_Adult', False):
            return 'Adult'
        else:
            return 'Young'

    filtered_df['AgeGroup'] = filtered_df.apply(resolve_age_group, axis=1)
    age_churn = filtered_df.groupby('AgeGroup')['Exited'].mean().sort_values(ascending=False)
    fig3, ax3 = plt.subplots()
    sns.barplot(x=age_churn.index, y=age_churn.values, ax=ax3, palette=custom_colors)
    ax3.set_ylabel("Churn Rate")
    st.pyplot(fig3)

# Churn by Number of Products
if 'NumOfProducts' in filtered_df.columns:
    st.header("💳 Churn Rate by Number of Bank Products")
    prod_churn = filtered_df.groupby('NumOfProducts')['Exited'].mean()
    fig4, ax4 = plt.subplots()
    sns.barplot(x=prod_churn.index.astype(str), y=prod_churn.values, ax=ax4, palette=custom_colors)
    ax4.set_xlabel("Number of Products")
    ax4.set_ylabel("Churn Rate")
    st.pyplot(fig4)

# Engaged Customers
if 'EngagedCustomer' in filtered_df.columns:
    st.header("🚀 Churn Rate by Engagement")
    engaged_churn = filtered_df.groupby('EngagedCustomer')['Exited'].mean().rename({0: 'Not Engaged', 1: 'Engaged'})
    fig5, ax5 = plt.subplots()
    sns.barplot(x=engaged_churn.index, y=engaged_churn.values, ax=ax5, palette=custom_colors)
    ax5.set_ylabel("Churn Rate")
    st.pyplot(fig5)

# Feature Importance
st.header("📈 Feature Importance (XGBoost)")
fig6, ax6 = plt.subplots(figsize=(10, 6))
plot_importance(xgb2, max_num_features=10, importance_type='gain', ax=ax6)
st.pyplot(fig6)

# Live Prediction
st.header("Customer Churn Predictor")
with st.form("prediction_form"):
    st.subheader("Enter Customer Information:")
    credit_score = st.slider("Credit Score", 300, 900, 650)
    age = st.slider("Age", 18, 100, 40)
    tenure = st.slider("Tenure (Years with Bank)", 0, 10, 3)
    balance = st.number_input("Balance", 0.0, 300000.0, step=1000.0)
    num_products = st.selectbox("Number of Bank Products", [1, 2, 3, 4])
    has_cr_card = st.selectbox("Has Credit Card?", ["Yes", "No"])
    is_active = st.selectbox("Is Active Member?", ["Yes", "No"])
    estimated_salary = st.number_input("Estimated Salary", 0.0, 300000.0, step=1000.0)
    geography = st.selectbox("Geography", ["France", "Germany", "Spain"])
    gender = st.selectbox("Gender", ["Male", "Female"])
    submit = st.form_submit_button("Predict")

if submit:
    gender = 1 if gender == "Male" else 0
    has_cr_card = 1 if has_cr_card == "Yes" else 0
    is_active = 1 if is_active == "Yes" else 0
    geography_germany = 1 if geography == "Germany" else 0
    geography_spain = 1 if geography == "Spain" else 0
    agegroup_adult = 1 if 30 < age <= 50 else 0
    agegroup_senior = 1 if age > 50 else 0
    engaged = 1 if is_active == 1 and num_products > 1 else 0

    input_data = pd.DataFrame([[
        credit_score, gender, age, tenure, balance, num_products,
        has_cr_card, is_active, estimated_salary,
        geography_germany, geography_spain,
        engaged, agegroup_adult, agegroup_senior
    ]],columns = [
    'CreditScore', 'Gender', 'Age', 'Tenure', 'Balance', 'NumOfProducts',
    'HasCrCard', 'IsActiveMember', 'EstimatedSalary',
    'Geography_Germany', 'Geography_Spain',
    'AgeGroup_Adult', 'AgeGroup_Senior', 'EngagedCustomer'  # Correct order!
    ])

    prediction = xgb2.predict(input_data)[0]
    proba = xgb2.predict_proba(input_data)[0][1]

    st.subheader("🔍 Prediction Result:")
    st.markdown(f"**Churn Prediction:** {'Churned' if prediction == 1 else 'Stayed'}")
    st.markdown(f"**Probability of Churn:** {proba:.2%}")

# Footer
st.markdown("---")
st.caption("DataScience Project Mussa")
