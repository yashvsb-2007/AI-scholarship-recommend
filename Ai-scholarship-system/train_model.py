import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import joblib

# Load Dataset
data = pd.read_csv("dataset/scholarships.csv")

# Convert text values to numbers
community_map = {
    "OC": 0,
    "BC": 1,
    "MBC": 2,
    "SC": 3,
    "ST": 4,
    "Any": 5
}

department_map = {
    "CSBS": 0,
    "CSE": 1,
    "Any": 2
}

data["Community"] = data["Community"].map(community_map)
data["Department"] = data["Department"].map(department_map)

# Features
X = data[["Minimum_CGPA", "Maximum_Income", "Community", "Department"]]

# Target
y = data["Scholarship"]

# Train Model
model = DecisionTreeClassifier()
model.fit(X, y)

# Save Model
joblib.dump(model, "scholarship_model.pkl")

print("✅ AI Model Trained Successfully!")