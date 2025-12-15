# 💼 Customer Churn Prediction Dashboard

This project delivers an end-to-end customer churn prediction system for a retail bank, combining machine learning with an interactive dashboard to support data-driven customer retention decisions. The solution identifies high-risk customers, explains churn drivers, and enables live churn probability estimation through a deployed Streamlit application.


🔗 **[Click here to view the live dashboard](https://customer-churn-prediction-mussa.streamlit.app/)**


## Project Summary

The objective of this project is to predict customer churn and provide actionable insights to improve customer retention strategies in a banking context.

The solution includes:
- **Exploratory Data Analysis** to uncover churn patterns across demographics, geography, account activity, and product usage.
- **Feature Engineering**, including behavioural indicators such as `EngagedCustomer` and age segmentation.
- **Model Development and Comparison**, evaluating Logistic Regression and XGBoost models.
- **Model Selection**, where XGBoost was chosen due to superior recall and ROC-AUC, prioritising churn detection.
- **Deployment**, delivering an interactive Streamlit dashboard for analytics and real-time churn prediction.


## Model Performance

The final XGBoost model achieved:
- **ROC-AUC:** 84.85
- **Recall (Churn Class):** 85%
- **Accuracy:** 85%

Recall was prioritised to minimise false negatives, ensuring at-risk customers are correctly identified for retention interventions.




## Live Dashboard

You can explore the dashboard here:  
👉 [https://datascienceprojects-customerchurnpredictor.streamlit.app](https://customer-churn-prediction-mussa.streamlit.app/)

### Key Features:
- 📊 Churn analysis by age group, geography, products, and engagement
- 🎚️ Interactive filters (Gender and Geography)
- 🔮 Live prediction form for new customers



## Dashboard Screenshot

![Customer Churn Dashboard Screenshot 1](Screenshot_1.png)
![Customer Churn Dashboard Screenshot 2](Screenshot_2.png)
![Customer Churn Dashboard Screenshot 3](Screenshot_3.png)


## Churn Predictor App
![Customer_Churn_Predictor](Churn_Predictor.png)

## Running the Project Locally

```bash
# Clone the repository
git clone https://github.com/MusaIP12/customer-churn-prediction.git

# Navigate to the project directory
cd customer-churn-prediction

# Install dependencies
pip install -r requirements.txt

# Launch the dashboard
python -m streamlit run churn_dashboard.py


