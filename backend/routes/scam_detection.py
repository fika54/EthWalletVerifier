# backend/routes/scam_detection.py

from flask import Blueprint, request, jsonify
from services.nlp_service import analyze_text

# Create a Blueprint for scam detection routes
scam_bp = Blueprint('scam_bp', __name__)

@scam_bp.route('/detect-scam', methods=['POST'])
def detect_scam():
    # Expecting JSON input like: {"message": "some text"}
    data = request.json or {}
    message = data.get('message', '')

    if not message:
        return jsonify({"error": "No message provided"}), 400

    # >>> WRITE YOUR CODE HERE <<<
    # Call your analyze_text function to get results
    # For example:
    is_scam, confidence = analyze_text(message)
    
    # Then return a JSON response
    return jsonify({
        "message": message,
        "is_scam": is_scam,
        "confidence": confidence
    })
