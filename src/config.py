"""Central configuration: column schema, theme colors, priority bands, labels.

Keeping these constants in one place lets every page share the same vocabulary
for columns, colors and business rules.
"""

# ---------------------------------------------------------------------------
# Brand / theme colors (professional banking palette)
# ---------------------------------------------------------------------------
COLORS = {
    "primary": "#1B3A6B",      # deep blue
    "primary_light": "#2E5A9C",
    "accent": "#0E7C7B",       # teal accent
    "white": "#FFFFFF",
    "light_grey": "#F4F6FA",
    "grey": "#8A94A6",
    "high": "#1E8E3E",         # green  -> high priority lead
    "medium": "#F4B400",       # yellow -> medium priority lead
    "low": "#9AA0A6",          # grey   -> low priority lead
    "danger": "#D93025",
}

PRIORITY_COLORS = {
    "High": COLORS["high"],
    "Medium": COLORS["medium"],
    "Low": COLORS["low"],
}

# ---------------------------------------------------------------------------
# Lead priority thresholds (on predicted probability 0..1)
# ---------------------------------------------------------------------------
HIGH_THRESHOLD = 0.70
MEDIUM_THRESHOLD = 0.40


def priority_band(score: float) -> str:
    """Map a probability score to a lead priority band."""
    if score >= HIGH_THRESHOLD:
        return "High"
    if score >= MEDIUM_THRESHOLD:
        return "Medium"
    return "Low"


def recommended_action(score: float) -> str:
    """Suggest a marketing action based on the lead score band."""
    band = priority_band(score)
    if band == "High":
        return "Contact now - personalized loan offer"
    if band == "Medium":
        return "Nurture - follow-up email / call"
    return "Deprioritize - no direct outreach"


# ---------------------------------------------------------------------------
# Column schema
# ---------------------------------------------------------------------------
# Canonical target column name used internally.
TARGET = "Personal Loan"

# Columns that carry no predictive value and should be dropped if present.
DROP_COLUMNS = ["ID", "ZIP Code", "ZIPCode", "Zip Code", "ZIP", "Customer ID"]

# Maps many possible source header spellings -> canonical names.
# Comparison is done on a normalized (lowercased, stripped, no separators) key.
COLUMN_ALIASES = {
    "id": "ID",
    "customerid": "ID",
    "age": "Age",
    "experience": "Experience",
    "income": "Income",
    "zipcode": "ZIP Code",
    "zip": "ZIP Code",
    "family": "Family",
    "familysize": "Family",
    "ccavg": "CCAvg",
    "creditcardaverage": "CCAvg",
    "avgcreditcardspending": "CCAvg",
    "education": "Education",
    "mortgage": "Mortgage",
    "personalloan": "Personal Loan",
    "loan": "Personal Loan",
    "securitiesaccount": "Securities Account",
    "securities": "Securities Account",
    "cdaccount": "CD Account",
    "cd": "CD Account",
    "online": "Online",
    "onlinebanking": "Online",
    "creditcard": "CreditCard",
    "hascreditcard": "CreditCard",
}

# Human-friendly labels for displaying feature names.
FEATURE_LABELS = {
    "Age": "Age",
    "Experience": "Experience (years)",
    "Income": "Income (k$)",
    "Family": "Family size",
    "CCAvg": "Avg credit-card spend (k$)",
    "Education": "Education level",
    "Mortgage": "Mortgage value (k$)",
    "Securities Account": "Securities account",
    "CD Account": "CD account",
    "Online": "Online banking",
    "CreditCard": "Owns credit card",
}

MODEL_NAMES = ["Logistic Regression", "Random Forest", "XGBoost"]
