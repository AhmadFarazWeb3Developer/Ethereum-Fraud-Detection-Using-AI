import streamlit as st
import numpy as np
import pandas as pd
import pickle

# ------------------ Page Config ------------------
st.set_page_config(
    page_title="Ethereum Address Risk Assessment",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------ Load Models ------------------
def load_models():
    try:
        with open('random_forest_model.pkl', 'rb') as f:
            rf_model = pickle.load(f)
    except FileNotFoundError:
        rf_model = None

    try:
        with open('logistic_regression_model.pkl', 'rb') as f:
            lr_model = pickle.load(f)
    except FileNotFoundError:
        lr_model = None

    try:
        with open('scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)
    except FileNotFoundError:
        scaler = None

    return rf_model, lr_model, scaler

# ------------------ Load Dataset ------------------
def load_dataset():
    try:
        df = pd.read_csv('Cleaned_Ethereum_Fraud_Detection.csv')
        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
            .str.replace(' ', '_')
            .str.replace('(', '', regex=False)
            .str.replace(')', '', regex=False)
        )
        features_df = df.select_dtypes(include=['int64', 'float64']).drop(
            columns=['flag'], errors='ignore'
        )
        return features_df, df
    except FileNotFoundError:
        return None, None

rf_model, lr_model, scaler = load_models()
features_df, full_df = load_dataset()
feature_columns = features_df.columns.tolist() if features_df is not None else []

# ------------------ Styling ------------------
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Roboto+Mono:wght@400;500&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

st.markdown("""
<style>
* {
    color: white !important;
}

.stApp {
    background: #050117 !important;
}

section[data-testid="stSidebar"] {
    background: #050117 !important;
    border-right: 1px solid rgba(255, 255, 255, 0.1);
}

.header-box {
    background: #050117;
    padding: 10px;
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    margin-bottom: 24px;
}

.header-box h1 {
    font-size: 2.4rem;
    font-weight: 600;
    margin: 0;
}

.header-box p {
    margin-top: 8px;
    font-size: 1rem;
}

[data-testid="stMetric"] {
    background: #050117;
    padding: 16px;
    border-radius: 6px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.stNumberInput > div > div {
    background: #050117;
    border-radius: 6px;
    border: 1px solid rgba(255, 255, 255, 0.15);
}

.stNumberInput > div > input {
    background: #050117;
    font-family: 'Roboto Mono', monospace;
}

.stButton > button {
    background: #050117;
    font-weight: 500;
    font-size: 1rem;
    padding: 12px 24px;
    border-radius: 6px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    width: 100%;
    margin-top: 16px;
}

.stButton > button:hover {
    background: rgba(255, 255, 255, 0.05);
}

.pred-card {
    background: #050117;
    border-radius: 8px;
    padding: 32px;
    margin: 32px auto;
    max-width: 800px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.pred-card h3 {
    font-size: 1.8rem;
    margin: 0 0 8px 0;
    font-weight: 600;
    text-align: center;
}

.pred-card p {
    font-size: 1.1rem;
    margin: 0;
    text-align: center;
    font-family: 'Roboto Mono', monospace;
}

table {
    background: #050117;
    border-radius: 6px;
    width: 100%;
}

th {
    padding: 12px;
    font-weight: 500;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

td {
    padding: 10px 12px;
    font-family: 'Roboto Mono', monospace;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

hr {
    border: none;
    height: 1px;
    background: rgba(255, 255, 255, 0.1);
    margin: 24px 0;
}
</style>
""", unsafe_allow_html=True)

# --------------- Header ------------------
st.markdown("""
<div class="header-box">
    <h1>Ethereum Address Risk Assessment</h1>
    <p>Ethereum Address Risk Assessment using Machine Learning</p>
</div>
""", unsafe_allow_html=True)

# ------------------ Sidebar ------------------
with st.sidebar:
    st.header("Model Overview")
    st.metric("Features Used", f"{len(feature_columns)}")
    st.metric("Dataset Size", "9,843")
    st.subheader("Models")
    st.write("""
**Random Forest (Primary)**  
- 200 trees  
- Non-linear pattern detection  
- Accuracy: 92%  
- ROC-AUC: 0.94  

**Logistic Regression (Baseline)**  
- Linear classifier  
- Interpretable results  
- Accuracy: 85%  
- ROC-AUC: 0.88
""")

# ------------------ Inputs ------------------
st.markdown("### Enter Ethereum Address Details")
essential_fields = {
    'sent_tnx': 'Transactions Sent',
    'received_tnx': 'Transactions Received',
    'total_ether_sent': 'Total ETH Sent',
    'total_ether_received': 'Total ETH Received',
    'total_erc20_tnxs': 'Total ERC20 Transactions'
}

available_essential = {}
for key, label in essential_fields.items():
    for col in feature_columns:
        if key in col.lower():
            available_essential[col] = label
            break

if len(available_essential) < 3:
    available_essential = {feature_columns[i]: f"Feature {i+1}" 
                           for i in range(min(5, len(feature_columns)))}

user_inputs_display = {}
col_a, col_b = st.columns(2)
for idx, (feature, label) in enumerate(available_essential.items()):
    target_col = col_a if idx % 2 == 0 else col_b
    with target_col:
        min_val = float(full_df[feature].min()) if full_df is not None else 0.0
        max_val = float(full_df[feature].max()) if full_df is not None else 10000.0
        median_val = float(full_df[feature].median()) if full_df is not None else 0.0
        user_inputs_display[feature] = st.number_input(
            label=label, min_value=min_val, max_value=max_val,
            value=median_val if median_val>0 else 10.0, step=1.0
        )

# Build feature vector
user_inputs = {}
for feature in feature_columns:
    user_inputs[feature] = user_inputs_display.get(feature, 
                                float(full_df[feature].median()) if full_df is not None else 0.0)

# ------------------ Prediction ------------------
st.divider()
predict_button = st.button('Predict Fraud Risk')

if predict_button:
    if rf_model is None or not feature_columns:
        st.error("Model or features not loaded correctly.")
    else:
        X = np.array([[user_inputs[col] for col in feature_columns]])

        # Random Forest
        rf_pred = rf_model.predict(X)[0]
        rf_prob = rf_model.predict_proba(X)[0]
        fraud_prob = rf_prob[1]

        # Prediction Card
        result_text = 'FRAUDULENT - HIGH RISK' if rf_pred==1 else 'LEGITIMATE - LOW RISK'
      
        st.markdown(f"""
        <div class="pred-card" style="">
            <h3>{result_text}</h3>
            <p>Fraud Probability: {fraud_prob:.1%}</p>
        </div>
        """, unsafe_allow_html=True)

        # Logistic Regression Comparison
        if lr_model and scaler:
            X_scaled = scaler.transform(X)
            lr_pred = lr_model.predict(X_scaled)[0]
            lr_prob = lr_model.predict_proba(X_scaled)[0]
            comp_df = pd.DataFrame({
                'Model': ['Random Forest', 'Logistic Regression'],
                'Prediction': ['Fraudulent' if rf_pred==1 else 'Legitimate',
                               'Fraudulent' if lr_pred==1 else 'Legitimate'],
                'Fraud Probability': [f"{rf_prob[1]:.1%}", f"{lr_prob[1]:.1%}"]
            })
            st.markdown("<h4>Model Comparison</h4>", unsafe_allow_html=True)
            st.table(comp_df)