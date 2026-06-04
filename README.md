# 🏦 BankLead AI — AI Lead Scoring for Banking

BankLead AI is a clean, professional **Streamlit** web app that helps retail
banks identify high-potential customers for **personal-loan** campaigns using
AI-based customer analytics. Instead of mass marketing, marketing teams can
rank customers by a **lead score** and focus on the most promising segments.

> Research theme: *AI-based customer analytics for potential customer
> identification in banking using customer profile data.*

## ✨ Features

1. **Upload & Preview** — CSV upload with record/variable counts, sample
   preview, missing-value summary and target distribution.
2. **Automatic preprocessing** — drops non-predictive columns (ID, ZIP Code),
   fixes negative `Experience`, imputes missing values, stratified train/test
   split, scaling for Logistic Regression, raw features for tree models.
3. **Model training** — Logistic Regression, Random Forest, XGBoost with
   **class-imbalance handling** (balanced class weights / `scale_pos_weight`).
4. **Evaluation dashboard** — Accuracy, Precision, Recall, F1, ROC-AUC,
   PR-AUC, plus **Precision@Top 5/10/20%** and **Lift@Top 5/10/20%**. The best
   model is chosen by PR-AUC + top-k lead performance.
5. **Lead scoring** — per-customer acceptance probability, priority bands
   (High ≥ 0.70, Medium 0.40–0.69, Low < 0.40) and recommended actions.
6. **Top-lead selection** — Top 5% / 10% / 20% or a custom count.
7. **Customer insights** — feature importance (tree importances or LR
   coefficient direction), high-priority segment profile, education mix.
8. **Campaign recommendations** — plain-language marketing guidance.
9. **Export** — download ranked leads as **CSV** or **Excel**.

## 🎨 Design

Professional banking palette — deep blue, white, light grey; green/yellow/grey
for High/Medium/Low lead priority. Dashboard-driven, minimal and practical.

## 🚀 Quick start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. (Optional) generate a synthetic sample dataset
python sample_data/generate_sample.py

# 3. Run the app
streamlit run app.py
```

Then open the URL Streamlit prints (default http://localhost:8501).

In the app: **Upload & Preview → Load sample dataset** (or upload your own CSV)
→ **Train & Evaluate** → **Lead Scoring** → **Customer Insights** →
**Export Results**.

## 📥 Expected input columns

CSV at customer level. Recognized columns (flexible header matching):

| Demographic | Financial | Target |
|---|---|---|
| Age, Experience, Income, Family, Education | CCAvg, Mortgage, Securities Account, CD Account, Online, CreditCard | **Personal Loan** (1 = accepted, 0 = not) |

`ID` and `ZIP Code` are dropped automatically. This matches the well-known
*UniversalBank* personal-loan dataset.

## 🧱 Project structure

```
app.py                       # Page 1: Main dashboard
pages/
  1_Upload_and_Preview.py    # Page 2
  2_Train_and_Evaluate.py    # Page 3
  3_Lead_Scoring.py          # Page 4
  4_Customer_Insights.py     # Page 5
  5_Export_Results.py        # Page 6
src/
  config.py                  # schema, colors, priority rules
  preprocessing.py           # load / clean / split / scale
  modeling.py                # train models + importances
  metrics.py                 # metrics incl. precision@k / lift@k / PR-AUC
  scoring.py                 # lead table, segments, recommendations
  ui.py                      # shared theming helpers
sample_data/
  generate_sample.py         # synthetic dataset generator
```

## 🛠 Tech stack

Streamlit · Pandas · NumPy · scikit-learn · XGBoost · Plotly · OpenPyXL

## 📌 MVP scope

CSV upload, preview, auto preprocessing, three models, performance comparison,
lead scoring, top-lead selection, feature importance, CSV/Excel export. Future
work: CRM integration, real-time scoring, authentication, campaign automation.
