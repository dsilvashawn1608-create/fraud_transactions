from pymongo import MongoClient
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import joblib

# -------------------------------
# 1. MongoDB Connection
# -------------------------------
import sys
from pymongo.errors import ServerSelectionTimeoutError

try:
    client = MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=5000)
    # trigger server selection to fail fast if MongoDB isn't available
    client.server_info()
except ServerSelectionTimeoutError:
    print("ERROR: cannot connect to MongoDB at mongodb://localhost:27017.\n"
          "Start MongoDB or point `MongoClient` to a running instance.\n"
          "Options:\n"
          " - Start local MongoDB service (Windows): `net start MongoDB`\n"
          " - Run MongoDB in Docker: `docker run -d -p 27017:27017 --name mongodb mongo:6`\n"
          " - Run MongoDB inside WSL and run this script inside WSL/VS Code Remote - WSL.\n")
    sys.exit(1)

db = client["cscorner"]
collection = db["sample"]

data = list(collection.find({}, {"_id": 0}))
df = pd.DataFrame(data)

# Validate data
required_cols = {"step", "type", "amount", "oldbalanceOrg", "newbalanceOrig",
                 "oldbalanceDest", "newbalanceDest", "isFraud"}

if df.empty:
    print("ERROR: the MongoDB collection 'cscorner.sample' is empty.\n"
          "Populate the collection with transaction documents or point the script to a dataset.\n"
          "Example to import JSON (from host):\n"
          "  mongoimport --uri mongodb://localhost:27017/cscorner --collection sample --file sample.json --jsonArray\n")
    sys.exit(1)

missing = required_cols.difference(df.columns)
if missing:
    print(f"ERROR: the dataset is missing required fields: {sorted(list(missing))}\n"
          "Ensure your documents include these keys or update `features` in the script.")
    sys.exit(1)

# -------------------------------
# 2. Encoding
# -------------------------------
le = LabelEncoder()
df["type"] = le.fit_transform(df["type"])

# -------------------------------
# 3. Feature Engineering (BIG BOOST)
# -------------------------------
df["amount_ratio_org"] = df["amount"] / (df["oldbalanceOrg"] + 1)
df["amount_ratio_dest"] = df["amount"] / (df["oldbalanceDest"] + 1)
df["balance_diff_org"] = df["oldbalanceOrg"] - df["newbalanceOrig"]
df["balance_diff_dest"] = df["oldbalanceDest"] - df["newbalanceDest"]

features = [
    "step", "type", "amount",
    "oldbalanceOrg", "newbalanceOrig",
    "oldbalanceDest", "newbalanceDest",
    "amount_ratio_org", "amount_ratio_dest",
    "balance_diff_org", "balance_diff_dest"
]

X = df[features]
y = df["isFraud"]

# -------------------------------
# 4. Train/Test Split (IMPORTANT)
# -------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# -------------------------------
# 5. Improved RandomForest
# -------------------------------
model = RandomForestClassifier(
    n_estimators=300,
    max_depth=12,
    min_samples_split=10,
    min_samples_leaf=5,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# -------------------------------
# 6. Evaluation
# -------------------------------
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("ROC-AUC Score:", roc_auc_score(y_test, y_proba))

# -------------------------------
# 7. Save Model
# -------------------------------
joblib.dump(model, "fraud_model.pkl")
joblib.dump(le, "type_encoder.pkl")

print("\n✅ Improved model and encoder saved")
