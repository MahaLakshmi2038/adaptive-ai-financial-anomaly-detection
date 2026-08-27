import pandas as pd
import os

from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import IsolationForest
from sklearn.pipeline import Pipeline


# ============================================================
# 1. FILE PATHS
# ============================================================

DATA_FILE = "data/finance_fraud_data.csv"
OUTPUT_FILE = "results/anomaly_results.csv"
ADAPTIVE_CONFIG_FILE = "results/adaptive_config.csv"


# ============================================================
# 2. LOAD DATASET
# ============================================================

df = pd.read_csv(DATA_FILE)

print("Dataset loaded successfully.")
print("Total transactions:", len(df))


# ============================================================
# 3. LOAD ADAPTIVE THRESHOLD
# ============================================================

base_threshold = 40

if os.path.exists(ADAPTIVE_CONFIG_FILE):

    try:
        config = pd.read_csv(ADAPTIVE_CONFIG_FILE)

        threshold_row = config[
            config["Parameter"] == "Risk_Threshold"
        ]

        if not threshold_row.empty:
            adaptive_threshold = float(
                threshold_row.iloc[0]["Value"]
            )
        else:
            adaptive_threshold = base_threshold

    except Exception:
        adaptive_threshold = base_threshold

else:
    adaptive_threshold = base_threshold


# Keep threshold within a sensible range
adaptive_threshold = max(
    30,
    min(adaptive_threshold, 60)
)

print(
    "Adaptive risk threshold:",
    adaptive_threshold
)


# ============================================================
# 4. DATA PREPROCESSING
# ============================================================

df["Timestamp"] = pd.to_datetime(
    df["Timestamp"]
)

df["Hour"] = df["Timestamp"].dt.hour
df["DayOfWeek"] = df["Timestamp"].dt.dayofweek


# ============================================================
# 5. SELECT FEATURES
# ============================================================

features = [
    "Amount",
    "Distance_from_Home",
    "IP_Risk_Score",
    "Avg_Spending_Habit",
    "Is_Weekend",
    "Is_Night_Transaction",
    "Hour",
    "DayOfWeek",
    "Merchant_Category",
    "Device_Type"
]

X = df[features]


# ============================================================
# 6. NUMERICAL + CATEGORICAL FEATURES
# ============================================================

numeric_features = [
    "Amount",
    "Distance_from_Home",
    "IP_Risk_Score",
    "Avg_Spending_Habit",
    "Is_Weekend",
    "Is_Night_Transaction",
    "Hour",
    "DayOfWeek"
]

categorical_features = [
    "Merchant_Category",
    "Device_Type"
]


# ============================================================
# 7. PREPROCESSING PIPELINE
# ============================================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "num",
            StandardScaler(),
            numeric_features
        ),
        (
            "cat",
            OneHotEncoder(
                handle_unknown="ignore"
            ),
            categorical_features
        )
    ]
)


# ============================================================
# 8. ISOLATION FOREST
# ============================================================

model = IsolationForest(
    n_estimators=150,
    contamination=0.12,
    random_state=42
)


# ============================================================
# 9. COMPLETE ML PIPELINE
# ============================================================

pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("model", model)
])


# ============================================================
# 10. TRAIN MODEL
# ============================================================

pipeline.fit(X)

print(
    "Isolation Forest model trained successfully."
)


# ============================================================
# 11. DETECT ANOMALIES
# ============================================================

df["Anomaly"] = pipeline.predict(X)

df["Anomaly"] = df["Anomaly"].map({
    1: 0,
    -1: 1
})


# ============================================================
# 12. BEHAVIORAL DEVIATION
# ============================================================

df["Spending_Deviation"] = (
    abs(
        df["Amount"]
        - df["Avg_Spending_Habit"]
    )
    /
    (
        df["Avg_Spending_Habit"]
        + 1
    )
)

deviation_score = (
    df["Spending_Deviation"]
    .clip(0, 1)
)


# ============================================================
# 13. IP RISK
# ============================================================

ip_score = (
    df["IP_Risk_Score"]
    .clip(0, 100)
    / 100
)


# ============================================================
# 14. HYBRID RISK SCORE
# ============================================================

df["Risk_Score"] = (
    0.5 * deviation_score
    + 0.3 * ip_score
    + 0.2 * df["Anomaly"]
)

df["Risk_Score"] = (
    df["Risk_Score"] * 100
).round(2)


# ============================================================
# 15. EXPLAINABLE RISK ANALYSIS
# ============================================================

def generate_explanation(row):

    reasons = []

    if row["Spending_Deviation"] >= 0.50:
        reasons.append(
            "Transaction amount significantly differs from spending habit"
        )

    elif row["Spending_Deviation"] >= 0.25:
        reasons.append(
            "Transaction amount differs from normal spending habit"
        )

    if row["IP_Risk_Score"] >= 70:
        reasons.append(
            "High-risk IP address"
        )

    elif row["IP_Risk_Score"] >= 40:
        reasons.append(
            "Elevated IP risk"
        )

    if row["Distance_from_Home"] >= 100:
        reasons.append(
            "Unusual transaction distance"
        )

    elif row["Distance_from_Home"] >= 50:
        reasons.append(
            "Transaction occurred far from usual location"
        )

    if row["Is_Night_Transaction"] == 1:
        reasons.append(
            "Night-time transaction"
        )

    if row["Is_Weekend"] == 1:
        reasons.append(
            "Weekend transaction"
        )

    if row["Anomaly"] == 1:
        reasons.append(
            "Machine-learning anomaly detected"
        )

    if not reasons:
        reasons.append(
            "Transaction behavior appears normal"
        )

    return " | ".join(reasons)


df["Risk_Explanation"] = df.apply(
    generate_explanation,
    axis=1
)


# ============================================================
# 16. ADAPTIVE RISK CLASSIFICATION
# ============================================================

# The adaptive threshold now controls
# future risk classification.

suspicious_threshold = adaptive_threshold

high_risk_threshold = adaptive_threshold + 15


# ============================================================
# 13. ADAPTIVE RISK CLASSIFICATION
# ============================================================

# Read the latest threshold learned from administrator feedback.

adaptive_threshold = 40

config_file = "results/adaptive_config.csv"

try:

    config = pd.read_csv(config_file)

    threshold_value = config.loc[
        config["Parameter"] == "Risk_Threshold",
        "Value"
    ]

    if len(threshold_value) > 0:
        adaptive_threshold = float(
            threshold_value.iloc[0]
        )

except Exception:

    print(
        "Adaptive configuration unavailable."
    )

    print(
        "Using default threshold:",
        adaptive_threshold
    )


print(
    "\nCurrent adaptive threshold:",
    adaptive_threshold
)


# High-risk threshold remains above
# the adaptive suspicious threshold.

high_risk_threshold = adaptive_threshold + 15


def classify_risk(score):

    if score >= high_risk_threshold:

        return "High Risk"

    elif score >= adaptive_threshold:

        return "Suspicious"

    else:

        return "Normal"


df["Risk_Level"] = (
    df["Risk_Score"].apply(
        classify_risk
    )
)

# ============================================================
# 17. CONCEPT DRIFT DETECTION
# ============================================================

# Compare anomaly behavior in the earlier
# and later parts of the transaction history.

df_sorted = df.sort_values(
    "Timestamp"
).copy()

split_point = int(
    len(df_sorted) * 0.70
)

historical_data = df_sorted.iloc[
    :split_point
]

recent_data = df_sorted.iloc[
    split_point:
]

historical_anomaly_rate = (
    historical_data["Anomaly"].mean()
    * 100
)

recent_anomaly_rate = (
    recent_data["Anomaly"].mean()
    * 100
)

drift_difference = (
    recent_anomaly_rate
    - historical_anomaly_rate
)


if abs(drift_difference) >= 3:

    drift_status = "Drift Detected"

else:

    drift_status = "Stable"


df["Historical_Anomaly_Rate"] = round(
    historical_anomaly_rate,
    2
)

df["Recent_Anomaly_Rate"] = round(
    recent_anomaly_rate,
    2
)

df["Drift_Status"] = drift_status


# ============================================================
# 18. DISPLAY RESULTS
# ============================================================

print("\n----------------------------------------")
print("ADAPTIVE ANOMALY DETECTION RESULTS")
print("----------------------------------------")

print(
    "\nTotal Transactions:",
    len(df)
)

print(
    "Detected Anomalies:",
    df["Anomaly"].sum()
)

print(
    "\nAdaptive Threshold:",
    adaptive_threshold
)

print(
    "High Risk Threshold:",
    high_risk_threshold
)

print(
    "\nRisk Distribution:"
)

print(
    df["Risk_Level"].value_counts()
)

print(
    "\nBehavioral Drift:"
)

print(
    "Historical anomaly rate:",
    round(
        historical_anomaly_rate,
        2
    ),
    "%"
)

print(
    "Recent anomaly rate:",
    round(
        recent_anomaly_rate,
        2
    ),
    "%"
)

print(
    "Drift status:",
    drift_status
)

print(
    "\nSample Results:"
)

print(
    df[
        [
            "Transaction_ID",
            "Amount",
            "Risk_Score",
            "Risk_Level",
            "Risk_Explanation"
        ]
    ].head(10)
)


# ============================================================
# 19. SAVE RESULTS
# ============================================================

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print(
    "\n----------------------------------------"
)

print(
    "Results saved to:"
)

print(
    OUTPUT_FILE
)

print(
    "----------------------------------------"
)