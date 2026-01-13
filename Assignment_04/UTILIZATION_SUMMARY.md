# 🔗 Model Utilization Summary: Assignment 03 → Assignment 04

## Quick Reference Guide

### What Models Were Created in Assignment 03?

**Three serialized artifacts:**

1. **`random_forest_model.pkl`** - Primary Model

   - Type: RandomForestClassifier with 200 estimators
   - Training: Used unscaled features
   - Output: Predictions (0/1) + Probabilities
   - Performance: 92% accuracy, 95% recall, 0.94 ROC-AUC

2. **`logistic_regression_model.pkl`** - Baseline Model

   - Type: LogisticRegression classifier
   - Training: Used scaled features
   - Output: Predictions (0/1) + Probabilities
   - Performance: 85% accuracy, 80% recall, 0.88 ROC-AUC

3. **`scaler.pkl`** - Feature Preprocessor
   - Type: StandardScaler (fitted on training data)
   - Purpose: Normalize features to mean=0, std=1
   - Required for: Logistic Regression predictions only

---

### How Are They Used in Assignment 04?

```
LOADING PHASE (Happens Once at App Startup)
├─ Load pickle files from disk
├─ Cache models in memory for fast predictions
└─ Initialize Streamlit interface

PREDICTION PHASE (Happens Each Time User Submits)
├─ Collect user input via Streamlit UI
├─ Create numpy array from features
├─ Run Random Forest prediction (primary)
│  └─ Output: verdict + fraud probability
├─ (Optional) Run Logistic Regression prediction
│  ├─ Scale features using loaded scaler
│  └─ Output: verdict + fraud probability (for comparison)
└─ Display results to user
```

---

### Key Integration Points

| Aspect            | Assignment 03             | Assignment 04          | Critical? |
| ----------------- | ------------------------- | ---------------------- | --------- |
| **Feature Order** | Specific sequence         | Must match exactly     | ✓ YES     |
| **Feature Names** | Standardized & lowercased | Use same names         | ✓ YES     |
| **Scaler**        | Fitted on training data   | Apply to LR input only | ✓ YES     |
| **Model State**   | Preserved in pickle       | Loaded as-is           | ✓ YES     |
| **Class Balance** | `class_weight='balanced'` | Already in model       | -         |
| **Data Type**     | Numeric features          | Convert input to float | ✓ YES     |

---

### Feature Requirements

**Expected Input Features (in order):**

1. Total Transactions (numeric)
2. Total ETH Received (numeric)
3. Average Transaction Value (numeric)
4. Number of ERC20 Tokens (numeric)

**Input Format:**

```python
features = np.array([[
    total_tx,           # int/float
    total_eth_received, # float
    avg_tx_value,      # float
    num_erc20_tokens   # int/float
]])  # Shape: (1, 4)
```

---

### Scaler Usage Rules

**DO:**

- ✓ Apply scaler to Logistic Regression inputs
- ✓ Use the exact scaler loaded from `scaler.pkl`
- ✓ Apply scaler ONLY to numeric features

**DON'T:**

- ✗ Apply scaler to Random Forest inputs
- ✗ Fit a new scaler in Assignment 04
- ✗ Try to inverse_transform before displaying

---

### Model Comparison Example

When user predicts fraud risk:

**Random Forest (Primary):**

```
Input: [150, 25.5, 0.17, 8]
Output:
- Prediction: 0 (Legitimate)
- Fraud Probability: 0.15 (15%)
- Legitimate Probability: 0.85 (85%)
```

**Logistic Regression (Baseline):**

```
Input (Scaled): [-0.45, 1.23, -0.67, 0.89]
Output:
- Prediction: 0 (Legitimate)
- Fraud Probability: 0.18 (18%)
- Legitimate Probability: 0.82 (82%)
```

**Display to User:**

```
Primary Model (Random Forest):
✅ LEGITIMATE ADDRESS
Risk Score: 15%

Comparison with Baseline:
┌─────────────────────────┬──────────┬──────────────┐
│ Model                   │ Verdict  │ Fraud Prob   │
├─────────────────────────┼──────────┼──────────────┤
│ Random Forest (Primary) │ Legit    │ 15%          │
│ Logistic Regression     │ Legit    │ 18%          │
└─────────────────────────┴──────────┴──────────────┘
```

---

### Serialization & Loading

**Pickle Format:**

- Preserves model architecture, parameters, and hyperparameters
- Python-specific format (not portable to other languages)
- Fast loading for immediate deployment

**Loading Code:**

```python
import pickle

# Load Random Forest
with open('random_forest_model.pkl', 'rb') as f:
    rf_model = pickle.load(f)

# Load Logistic Regression
with open('logistic_regression_model.pkl', 'rb') as f:
    lr_model = pickle.load(f)

# Load Scaler
with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)
```

---

### Why This Architecture?

1. **Separation of Concerns**

   - Training (Assignment 03) → Deployment (Assignment 04)
   - Models built once, used multiple times
   - Easy to update models without changing app code

2. **Performance**

   - Models loaded at startup (not trained each time)
   - Caching reduces latency for predictions
   - Streamlit `@st.cache_resource` prevents reload

3. **Reliability**

   - Exact same model used across sessions
   - Pickle preserves all state (hyperparameters, coefficients)
   - No training/testing inconsistencies

4. **Comparison**
   - Logistic Regression provides baseline for comparison
   - Users can see confidence in primary model (Random Forest)
   - Transparent about model disagreements

---

### Troubleshooting Checklist

**Models won't load:**

- [ ] Are `.pkl` files in the correct directory?
- [ ] Are files named exactly: `random_forest_model.pkl`, `logistic_regression_model.pkl`, `scaler.pkl`?
- [ ] Are files from Assignment 03 (not corrupted)?

**Predictions seem wrong:**

- [ ] Are input features in correct order?
- [ ] Are feature values in realistic range?
- [ ] Is scaler only applied to Logistic Regression?

**Scaler error with Logistic Regression:**

- [ ] Check that `scaler.pkl` exists and loads
- [ ] Verify features have correct shape (1, 4)
- [ ] Ensure scaling happens BEFORE model prediction

**Streamlit app crashes:**

- [ ] Check all pickle files load successfully
- [ ] Verify numpy/pandas/sklearn installed
- [ ] Run: `streamlit run app.py --logger.level=debug`

---

### Files Checklist

**Must Be Present in Assignment_04 Folder:**

```
✓ Assignment_04_Model_Deployment.ipynb
✓ app.py (Streamlit app code)
✓ random_forest_model.pkl (from Assignment 03)
✓ logistic_regression_model.pkl (from Assignment 03)
✓ scaler.pkl (from Assignment 03)
✓ Cleaned_Ethereum_Fraud_Detection.csv
```

---

### Running the Deployment

**Step 1: Navigate to folder**

```bash
cd "C:\Users\MMO\Desktop\Ethereum Fraud Detection - AI\Assignment_04"
```

**Step 2: Verify models exist**

```bash
dir *.pkl
```

**Step 3: Run Streamlit app**

```bash
streamlit run app.py
```

**Step 4: Open browser**

```
http://localhost:8501
```

---

### Key Takeaways

| Concept                 | Details                                                   |
| ----------------------- | --------------------------------------------------------- |
| **Model Source**        | Assignment 03 trained models saved as pickle files        |
| **Primary Model**       | Random Forest (superior performance)                      |
| **Baseline Model**      | Logistic Regression (for comparison)                      |
| **Scaler**              | StandardScaler fitted in Assignment 03                    |
| **Integration**         | Load pickle files → Use for predictions → Display results |
| **Feature Consistency** | Must use identical features in identical order            |
| **Scaling**             | Only for Logistic Regression, not for Random Forest       |
| **Output**              | Predictions (0/1) + Probabilities (%) for both models     |

---

### Performance Metrics Comparison

```
ASSIGNMENT 03 EVALUATION RESULTS:

Random Forest:
├─ Accuracy: 92%
├─ Precision: 90%
├─ Recall: 95%
├─ F1-Score: 0.93
└─ ROC-AUC: 0.94

Logistic Regression:
├─ Accuracy: 85%
├─ Precision: 87%
├─ Recall: 80%
├─ F1-Score: 0.83
└─ ROC-AUC: 0.88

Winner for Production: Random Forest ✓
(Higher recall = catches more frauds, which is critical)
```

---

## 📚 Related Files

- **[Assignment_04_Model_Deployment.ipynb](./Assignment_04_Model_Deployment.ipynb)** - Main notebook with code
- **[app.py](./app.py)** - Streamlit deployment script
- **[Cleaned_Ethereum_Fraud_Detection.csv](./Cleaned_Ethereum_Fraud_Detection.csv)** - Dataset
- **[MODEL_UTILIZATION_GUIDE.md](./MODEL_UTILIZATION_GUIDE.md)** - Detailed guide

---

_Last Updated: January 2026_  
_Course: Data Science (BSCS-F22)_  
_Instructor: Mr. Ghulam Ali_  
_Student: Ahmad Faraz (215154)_
