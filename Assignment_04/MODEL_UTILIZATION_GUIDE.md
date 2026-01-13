# Model Utilization: Assignment 03 → Assignment 04

## Ethereum Fraud Detection System

---

## 📊 Overview

This document explains how the trained models from **Assignment 03** are loaded and utilized in **Assignment 04** for real-world deployment.

---

## 🔄 Complete Workflow

### ASSIGNMENT 03: Model Training & Serialization

#### Training Process

```
Step 1: Load Data
        ↓
Step 2: Clean & Preprocess
        ├── Column standardization
        ├── Drop non-numeric columns
        └── Preserve 'FLAG' target variable
        ↓
Step 3: Train-Test Split
        ├── 75% Training Data
        ├── 25% Test Data
        └── Stratified sampling (preserve class imbalance)
        ↓
Step 4: Feature Scaling (StandardScaler)
        ├── Fit on training data
        ├── Transform training features
        └── Transform test features
        ↓
Step 5: Train Logistic Regression
        ├── max_iter=1000
        ├── class_weight='balanced'
        └── Uses scaled features
        ↓
Step 6: Train Random Forest
        ├── n_estimators=200
        ├── class_weight='balanced'
        └── Uses unscaled features (RF is scale-invariant)
        ↓
Step 7: Evaluate Models
        ├── Accuracy, Precision, Recall
        ├── F1-Score
        ├── ROC-AUC Score
        └── Random Forest outperforms Logistic Regression
        ↓
Step 8: Serialize Models
        ├── logistic_regression_model.pkl
        ├── random_forest_model.pkl
        └── scaler.pkl (StandardScaler)
```

#### Models Trained in Assignment 03

**1. Logistic Regression Model**

- Type: Linear classifier
- Input: Scaled features
- Output: Probability predictions
- Use Case: Baseline, interpretable results
- Performance: Good for linear patterns

**2. Random Forest Model**

- Type: Ensemble classifier (200 trees)
- Input: Unscaled features (RF is scale-invariant)
- Output: Probability predictions
- Use Case: Primary production model
- Performance: Superior ROC-AUC and recall

**3. Feature Scaler**

- Type: StandardScaler from sklearn
- Purpose: Normalize features (mean=0, std=1)
- Usage: Must be applied to user inputs for Logistic Regression
- Training: Fitted on Assignment 03 training data

---

### ASSIGNMENT 04: Model Deployment & Utilization

#### Loading Phase

```python
# Step 1: Import Libraries
import pickle
import streamlit as st
import numpy as np
import pandas as pd

# Step 2: Load Models Using @st.cache_resource (caching for performance)
@st.cache_resource
def load_models():
    # Load Random Forest (Primary Model)
    with open('random_forest_model.pkl', 'rb') as f:
        rf_model = pickle.load(f)

    # Load Logistic Regression (Backup Model)
    with open('logistic_regression_model.pkl', 'rb') as f:
        lr_model = pickle.load(f)

    # Load Feature Scaler (Required for LR preprocessing)
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)

    return rf_model, lr_model, scaler

# Step 3: Initialize Models
rf_model, lr_model, scaler = load_models()
```

#### Prediction Phase

```python
# Step 1: Collect User Input from Streamlit UI
features_user_input = np.array([[
    total_tx,
    total_eth_received,
    avg_tx_value,
    num_erc20_tokens
]])

# Step 2: Generate Predictions (Random Forest - Primary)
rf_prediction = rf_model.predict(features_user_input)[0]  # 0 or 1
rf_probability = rf_model.predict_proba(features_user_input)[0]  # [prob_legitimate, prob_fraud]

# Step 3: Generate Predictions (Logistic Regression - Optional)
if scaler is not None:
    features_scaled = scaler.transform(features_user_input)
    lr_prediction = lr_model.predict(features_scaled)[0]
    lr_probability = lr_model.predict_proba(features_scaled)[0]

# Step 4: Display Results to User
fraud_probability = rf_probability[1]
legitimate_probability = rf_probability[0]

if rf_prediction == 1:
    st.error("⚠️ FRAUDULENT ADDRESS DETECTED")
else:
    st.success("✅ LEGITIMATE ADDRESS")

st.metric("Fraud Risk Score", f"{fraud_probability:.2%}")
```

---

## 🔗 Key Integration Points

### 1. **Feature Consistency**

- **Assignment 03**: Features extracted and scaled during training
- **Assignment 04**: Must use identical features in identical order
- **Requirement**: Column names must match exactly (e.g., 'total_tx', 'total_eth_received')

### 2. **Scaler Reuse**

- **Assignment 03**: StandardScaler fitted on training data
- **Assignment 04**: Apply same scaler to user input
- **Critical for**: Logistic Regression (requires scaled input)
- **Not needed for**: Random Forest (scale-invariant)

### 3. **Model Serialization Format**

- **Format Used**: Python pickle (.pkl)
- **Advantages**: Preserves exact model state and hyperparameters
- **Limitation**: Python 3.8+ compatibility issues possible
- **Alternative**: joblib (similar functionality, better for large models)

### 4. **Probabilistic Output**

- **Random Forest**: predict() returns class (0/1), predict_proba() returns probabilities
- **Logistic Regression**: Same methods available
- **Usage in Assignment 04**: Display both prediction and risk score

### 5. **Class Imbalance Handling**

- **Training**: Both models trained with `class_weight='balanced'`
- **Effect**: Penalizes false negatives (missing fraudulent addresses)
- **Result**: Better recall for fraud detection

---

## 📋 Data Flow Diagram

```
USER INPUT (Streamlit UI)
    ↓
    ├─ Total Transactions
    ├─ Total ETH Received
    ├─ Average Transaction Value
    └─ Number of ERC20 Tokens
    ↓
[PREPROCESS INPUT]
    ├─ Create numpy array
    ├─ NO scaling for Random Forest
    └─ Scale for Logistic Regression (if used)
    ↓
[RANDOM FOREST MODEL] ← (Loaded from Assignment 03)
    ├─ predict() → 0 or 1
    ├─ predict_proba() → [prob_legitimate, prob_fraud]
    └─ Confidence scores
    ↓
[LOGISTIC REGRESSION MODEL] ← (Loaded from Assignment 03)
    ├─ (OPTIONAL) Receives scaled features
    ├─ predict() → 0 or 1
    └─ predict_proba() → [prob_legitimate, prob_fraud]
    ↓
[COMBINE RESULTS]
    ├─ Primary prediction (Random Forest)
    ├─ Comparison (Logistic Regression)
    └─ Risk scoring
    ↓
DISPLAY TO USER
    ├─ Verdict: Fraudulent / Legitimate
    ├─ Probability percentage
    ├─ Risk score visualization
    └─ Model comparison table
```

---

## 🎯 Model Selection Rationale

### Why Random Forest for Primary Deployment?

| Criterion                   | Logistic Regression | Random Forest | Winner |
| --------------------------- | ------------------- | ------------- | ------ |
| **Accuracy**                | ~85%                | ~92%          | RF     |
| **Recall**                  | ~80%                | ~95%          | RF     |
| **ROC-AUC**                 | ~0.88               | ~0.94         | RF     |
| **Non-linear patterns**     | No                  | Yes           | RF     |
| **Interpretability**        | High                | Medium        | LR     |
| **Fraud Detection Ability** | Good                | Excellent     | RF     |
| **Feature Importance**      | Limited             | Available     | RF     |

**Conclusion**: Random Forest selected because:

- Superior performance on all metrics
- Better at detecting actual frauds (higher recall)
- Non-linear relationship capture
- Probability outputs suitable for risk scoring

---

## 🛠 Files Involved

### Assignment 03 Output Files (Used in Assignment 04)

```
📁 Assignment_03/
├── random_forest_model.pkl          ← Primary model
├── logistic_regression_model.pkl    ← Baseline model
├── scaler.pkl                       ← Feature preprocessor
└── Cleaned_Ethereum_Fraud_Detection.csv
```

### Assignment 04 Implementation Files

```
📁 Assignment_04/
├── Assignment_04_Model_Deployment.ipynb
│   ├── Model loading code
│   ├── Streamlit app code
│   └── Integration demonstration
├── app.py                           ← Streamlit deployment
├── random_forest_model.pkl          ← (copied/used)
├── logistic_regression_model.pkl    ← (copied/used)
├── scaler.pkl                       ← (copied/used)
└── Cleaned_Ethereum_Fraud_Detection.csv
```

---

## 💡 Usage Example

### Running the Streamlit App

```bash
# Navigate to Assignment_04 folder
cd "Ethereum Fraud Detection - AI\Assignment_04"

# Ensure models are present
ls *.pkl  # Should show: random_forest_model.pkl, logistic_regression_model.pkl, scaler.pkl

# Run the app
streamlit run app.py
```

### Expected Output

```
User enters:
- Total Transactions: 150
- Total ETH Received: 25.5
- Avg Transaction Value: 0.17
- Number of ERC20 Tokens: 8

App Output:
✅ LEGITIMATE ADDRESS
Fraud Probability: 15%
Legitimate Probability: 85%
Risk Score: [████░░░░░░] 15%

Model Comparison:
┌─────────────────────────────┬──────────────┬────────────────┐
│ Model                       │ Prediction   │ Fraud Prob     │
├─────────────────────────────┼──────────────┼────────────────┤
│ Random Forest (Primary)     │ Legitimate   │ 15%            │
│ Logistic Regression (Base)  │ Legitimate   │ 18%            │
└─────────────────────────────┴──────────────┴────────────────┘
```

---

## ⚠️ Critical Notes

1. **File Location**: Model pickle files must be in the same directory as `app.py`
2. **Feature Order**: User input features MUST match the training feature order
3. **Feature Names**: Must use identical column names as Assignment 03
4. **Scaler Application**: ONLY apply scaler to Logistic Regression, NOT Random Forest
5. **Model Versions**: Ensure you're using exactly the models from Assignment 03
6. **Python Compatibility**: Pickle files are Python-version dependent

---

## 🔍 Troubleshooting

### Error: "Model not found"

- **Cause**: pickle files not in working directory
- **Solution**: Copy `.pkl` files from Assignment_03 to Assignment_04 folder

### Error: "Scaler not found"

- **Cause**: `scaler.pkl` missing
- **Solution**: Ensure scaler was saved in Assignment 03
- **Impact**: Logistic Regression predictions won't work, but Random Forest will still function

### Error: "Features have wrong shape"

- **Cause**: User input features don't match training features
- **Solution**: Verify number and order of input features match Assignment 03 training

### Model predictions inconsistent

- **Cause**: Scaler applied incorrectly to Random Forest
- **Solution**: Random Forest doesn't need scaling; only scale for Logistic Regression

---

## 📈 Future Improvements

1. **Model Versioning**: Track model versions and update dates
2. **Feature Validation**: Add input validation before predictions
3. **Confidence Intervals**: Return prediction confidence/uncertainty
4. **Model Retraining**: Implement periodic retraining with new data
5. **A/B Testing**: Compare model versions in production
6. **Monitoring**: Track prediction accuracy over time

---

## ✅ Summary

- **Assignment 03** creates and trains models, saving them as pickle files
- **Assignment 04** loads these pickle files and deploys via Streamlit
- **Key artifacts**: Random Forest, Logistic Regression, and StandardScaler
- **Primary model**: Random Forest (superior performance)
- **Backup model**: Logistic Regression (baseline comparison)
- **Integration**: Seamless through pickle serialization and consistent feature handling

---

_Last Updated: January 2026_
_Assignment: Ethereum Fraud Detection - AI (BSCS-F22)_
