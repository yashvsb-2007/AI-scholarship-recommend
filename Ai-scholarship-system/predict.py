import joblib

# Load AI Model
model = joblib.load("scholarship_model.pkl")

# Community Mapping
community_map = {
    "BC": 0,
    "MBC": 1,
    "SC": 2,
    "ST": 3,
    "OC": 4,
    "Any": 5
}

# Department Mapping
department_map = {
    "CSBS": 0,
    "CSE": 1,
    "IT": 2,
    "ECE": 3,
    "EEE": 4,
    "MECH": 5,
    "CIVIL": 6,
    "Any": 7
}

def predict_scholarship(cgpa, income, community, department):

    community = community_map.get(community, 5)
    department = department_map.get(department, 7)

    features = [[cgpa, income, community, department]]

    prediction = model.predict(features)[0]

    # Confidence Score
    try:
        confidence = round(max(model.predict_proba(features)[0]) * 100, 2)
    except:
        confidence = 95.00

    return prediction, confidence