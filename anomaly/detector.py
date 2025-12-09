import numpy as np
from sklearn.ensemble import IsolationForest
import joblib
import os

# Get the directory where this script is located
_MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
# Default to project root (parent of anomaly directory)
_PROJECT_ROOT = os.path.dirname(_MODULE_DIR)
# Use absolute path for model file
MODEL_FILE = os.environ.get("BAYANI_MODEL", os.path.join(_PROJECT_ROOT, "if_model.joblib"))

def train_sample_model():
    # sample training synthetic data: normal operations
    X = np.random.normal(loc=0.0, scale=1.0, size=(500, 2))
    model = IsolationForest(contamination=0.05, random_state=42)
    model.fit(X)
    joblib.dump(model, MODEL_FILE)
    return model

def load_model():
    if os.path.exists(MODEL_FILE):
        return joblib.load(MODEL_FILE)
    else:
        return train_sample_model()

def score_event(features, model=None):
    # features: list or array shape (n_features,)
    try:
        if model is None:
            model = load_model()
        
        # Ensure features is a list/array
        if not isinstance(features, (list, np.ndarray)):
            features = [float(features)]
        else:
            features = [float(f) for f in features]
        
        # Ensure we have the right number of features
        if len(features) != 2:
            # Pad or truncate to 2 features
            if len(features) < 2:
                features = features + [0.0] * (2 - len(features))
            else:
                features = features[:2]
        
        score = model.decision_function([features])[0]  # higher = more normal, lower = anomalous
        
        # Convert to anomaly_score in [0,1] where higher = more anomalous
        # IsolationForest decision_function typically returns values in range [-0.5, 0.5]
        # Normalize to [0, 1] where 1 = most anomalous
        min_score = -0.5
        max_score = 0.5
        if max_score - min_score == 0:
            normalized_score = 0.5
        else:
            normalized_score = 1.0 - ((score - min_score) / (max_score - min_score))
        
        # Clamp to [0, 1]
        normalized_score = max(0.0, min(1.0, normalized_score))
        return float(normalized_score)
    except Exception as e:
        print(f"Error scoring event: {e}")
        # Return a default score on error
        return 0.5

