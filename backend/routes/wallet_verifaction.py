# backend/routes/scam_detection.py

from flask import Blueprint, request, jsonify
from services.nlp_service import analyze_text

scam_bp = Blueprint('scam_bp', __name__)

@scam_bp.route('/detect-scam', methods=['POST'])
def detect_scam():
    """
    Analyzes the user's message to see if it's scammy using a trained NLP model.
    Expects JSON: { "message": "..." }
    """
    data = request.json or {}
    message = data.get('message', '')

    if not message:
        return jsonify({"error": "No message provided"}), 400

    # Use the NLP service
    is_scam, confidence = analyze_text(message)

    return jsonify({
        "message": message,
        "is_scam": is_scam,
        "confidence": round(confidence, 2)
    })

