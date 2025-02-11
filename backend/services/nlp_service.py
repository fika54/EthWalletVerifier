# backend/services/nlp_service.py

import pickle
import os

# >>> FILL HERE <<<
# Adjust the model filename if yours differs from "scam_model.pkl"
MODEL_PATH = os.path.join(
    os.path.dirname(__file__), '..', 'models', 'scam_model.pkl'
)

try:
    with open(MODEL_PATH, 'rb') as f:
        scam_model = pickle.load(f)
    print("Scam model loaded successfully from:", MODEL_PATH)
except Exception as e:
    scam_model = None
    print(f"Failed to load scam model: {e}")

def analyze_text(text):
    """
    Uses the loaded scikit-learn pipeline to classify 'text' as scam or legit.
    Returns (is_scam, confidence).
    """
    if not scam_model:
        # If the model can't be loaded, fallback
        return False, 0.0

    # >>> FILL HERE (Potentially) <<<
    # Check how your model was trained. Are classes "scam"/"legit" or something else?
    # If your label is different, you must adapt accordingly.

    prediction = scam_model.predict([text])[0]
    proba = scam_model.predict_proba([text])[0]

    classes = list(scam_model.classes_)  # e.g. ["legit", "scam"]

    # If "scam" is definitely in your classes, we do:
    if "scam" in classes:
        scam_index = classes.index("scam")
    else:
        # FILL HERE: If your classes are something else, do it accordingly
        scam_index = 0  # default to first if uncertain

    scam_probability = proba[scam_index]
    is_scam = (prediction == "scam")

    # Confidence is how sure we are
    confidence = scam_probability if is_scam else 1 - scam_probability

    return is_scam, float(confidence)

