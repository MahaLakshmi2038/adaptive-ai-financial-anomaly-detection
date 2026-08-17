import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import IsolationForest
from sklearn.pipeline import Pipeline

# ============================================================
# 1. LOAD DATASET
# ============================================================

df = pd.read_csv("data/finance_fraud_data.csv")

print("Dataset loaded successfully.")
print("Total transactions:", len(df))


# ============================================================
# 2. DATA PREPROCESSING
# ============================================================

# Convert timestamp into datetime format
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# Extract useful time-based features
df["Hour"] = df["Timestamp"].dt.hour
df["DayOfWeek"] = df["Timestamp"].dt.dayofweek


# ============================================================
# 3. SELECT FEATURES
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
# 4. DEFINE NUMERICAL AND CATEGORICAL FEATURES
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
# 5. PREPROCESSING PIPELINE
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
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        )
    ]
)


# ============================================================
# 6. ISOLATION FOREST
# ============================================================

model = IsolationForest(
    n_estimators=150,
    contamination=0.12,
    random_state=42
)


# ============================================================
# 7. COMPLETE ML PIPELINE
# ============================================================

pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("model", model)
])


# ============================================================
# 8. TRAIN MODEL
# ============================================================

pipeline.fit(X)

print("Isolation Forest model trained successfully.")


# ============================================================
# 9. DETECT ANOMALIES
# ============================================================

df["Anomaly"] = pipeline.predict(X)

# Isolation Forest:
#  1  = Normal
# -1  = Anomaly

df["Anomaly"] = df["Anomaly"].map({
    1: 0,
    -1: 1
})


# ============================================================
# 10. BEHAVIOURAL DEVIATION
# ============================================================

# Compare current transaction amount
# with the customer's average spending habit.

df["Spending_Deviation"] = (
    abs(df["Amount"] - df["Avg_Spending_Habit"])
    / (df["Avg_Spending_Habit"] + 1)
)

# Limit the deviation between 0 and 1
deviation_score = df["Spending_Deviation"].clip(0, 1)


# ============================================================
# 11. IP RISK SCORE
# ============================================================

# Convert IP risk from 0-100 into 0-1

ip_score = (
    df["IP_Risk_Score"].clip(0, 100) / 100
)


# ============================================================
# 12. HYBRID RISK SCORE
# ============================================================

# Combine:
# 50% behavioural deviation
# 30% IP risk
# 20% ML anomaly result

df["Risk_Score"] = (
    0.5 * deviation_score
    + 0.3 * ip_score
    + 0.2 * df["Anomaly"]
)

# Convert to percentage

df["Risk_Score"] = (
    df["Risk_Score"] * 100
).round(2)


# ============================================================
# 13. RISK CLASSIFICATION
# ============================================================

def classify_risk(score):

    if score >= 70:
        return "High Risk"

    elif score >= 40:
        return "Suspicious"

    else:
        return "Normal"


df["Risk_Level"] = (
    df["Risk_Score"].apply(classify_risk)
)


# ============================================================
# 14. DISPLAY RESULTS
# ============================================================

print("\n----------------------------------------")
print("ANOMALY DETECTION RESULTS")
print("----------------------------------------")

print("\nTotal Transactions:", len(df))

print(
    "Detected Anomalies:",
    df["Anomaly"].sum()
)


print("\nRisk Distribution:")

print(
    df["Risk_Level"].value_counts()
)


print("\nSample Results:")

print(
    df[
        [
            "Transaction_ID",
            "Amount",
            "Merchant_Category",
            "Risk_Score",
            "Risk_Level"
        ]
    ].head(10)
)


# ============================================================
# 15. SAVE RESULTS
# ============================================================

output_file = "results/anomaly_results.csv"

df.to_csv(
    output_file,
    index=False
)

print("\n----------------------------------------")
print("Results saved to:")
print(output_file)
print("----------------------------------------")