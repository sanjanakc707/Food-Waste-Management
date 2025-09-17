# train.py
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from joblib import dump
import os

os.makedirs("models", exist_ok=True)

# --- 1. Synthetic dataset generator ---
np.random.seed(42)
N = 8000

categories = ["vegetable","fruit","dairy","bread","meat","cooked"]
storage_types = ["fridge","freezer","pantry"]
opened = [0,1]

data = []
for _ in range(N):
    cat = np.random.choice(categories, p=[0.25,0.2,0.15,0.15,0.15,0.1])
    storage = np.random.choice(storage_types)
    is_open = np.random.choice(opened, p=[0.7,0.3])
    temp = {
        "fridge": 4 + np.random.randn()*1.5,
        "freezer": -18 + np.random.randn()*2,
        "pantry": 22 + np.random.randn()*4
    }[storage]
    days_since_purchase = max(0, int(abs(np.random.randn()*3 + {"vegetable":2,"fruit":3,"dairy":5,"bread":4,"meat":4,"cooked":3}[cat])))
    # baseline shelf-life (days)
    base = {"vegetable":7,"fruit":8,"dairy":10,"bread":5,"meat":6,"cooked":3}[cat]
    # storage factor
    storage_factor = {"fridge":0.9,"freezer":0.2,"pantry":1.1}[storage]
    open_factor = 1.3 if is_open else 1.0
    temp_factor = 1 + max(0, (temp - 5))/20  # hotter = faster spoil
    # days until spoil (ground truth)
    noise = np.random.randn()*1.8
    days_to_spoil = max(0, int(base*storage_factor/open_factor - days_since_purchase*0.5 - temp_factor + noise))
    # label reuse:
    # if bread/fruit/veg and not mold -> feed possible, dairy/meat/cooked -> compost or discard depending on heavy spoil
    # We'll create a simple rule and that becomes labels for classifier
    condition_quality = days_to_spoil  # proxy
    if cat in ["bread","fruit","vegetable"] and days_to_spoil >= 0:
        reuse = "feed"
    elif cat in ["dairy","meat","cooked"]:
        # often compost unless heavily spoiled -> discard
        reuse = "compost" if days_to_spoil >= -2 else "discard"
    else:
        reuse = "compost"

    data.append([cat, storage, is_open, round(temp,1), days_since_purchase, days_to_spoil, reuse])

df = pd.DataFrame(data, columns=["category","storage","opened","temp_C","days_since_purchase","days_to_spoil","reuse"])
# Small adjustments: if days_to_spoil <= -2 -> definitely discard
df.loc[df["days_to_spoil"] <= -2, "reuse"] = "discard"

# --- 2. Encode categorical features ---
enc_cat = LabelEncoder().fit(df["category"])
enc_storage = LabelEncoder().fit(df["storage"])
df["cat_enc"] = enc_cat.transform(df["category"])
df["stor_enc"] = enc_storage.transform(df["storage"])

features = ["cat_enc","stor_enc","opened","temp_C","days_since_purchase"]
X = df[features]
y_reg = df["days_to_spoil"]
y_clf = df["reuse"]

# --- 3. Train models ---
X_train, X_test, y_train_reg, y_test_reg = train_test_split(X, y_reg, test_size=0.15, random_state=42)
reg = RandomForestRegressor(n_estimators=150, random_state=42)
reg.fit(X_train, y_train_reg)

X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X, y_clf, test_size=0.15, random_state=42)
clf = RandomForestClassifier(n_estimators=200, random_state=42)
clf.fit(X_train_c, y_train_c)

# --- 4. Save models and encoders ---
dump(reg, "models/regressor.joblib")
dump(clf, "models/classifier.joblib")
dump({"cat":enc_cat, "storage":enc_storage}, "models/encoders.joblib")

print("Training done. Models saved to /models")
print("Sample rows:")
print(df.head())
