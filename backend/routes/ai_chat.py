import os
import requests
from flask import Blueprint, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("Error: OPENAI_API_KEY is not set in environment variables.")

client = OpenAI(api_key=OPENAI_API_KEY)


ai_chat_bp = Blueprint('ai_chat_bp', __name__)


SCAM_KEYWORDS = ["guaranteed returns", "double your crypto", "risk-free investment", "no loss", "get rich quick"]

def get_latest_crypto_scams():
    """Fetch recent scam reports from an external API."""
    try:
        response = requests.get("https://api.chainabuse.com/reports?category=crypto-scam")  
        data = response.json()
        scam_list = data.get("reports", [])
        
        latest_scams = []
        for scam in scam_list[:3]:  
            latest_scams.append(f"- **{scam['title']}**: {scam['description']} ({scam['date_reported']})")

        return "\n".join(latest_scams) if latest_scams else "No recent scam reports available."
    
    except Exception:
        return "⚠️ Could not retrieve live scam reports at this time."

@ai_chat_bp.route('/chat', methods=['POST'])
def chat_with_ai():
    """Handles user queries with AI and scam detection."""
    data = request.json or {}
    user_query = data.get("query", "").strip()

    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    scam_alert = any(keyword in user_query.lower() for keyword in SCAM_KEYWORDS)

    live_scam_data = get_latest_crypto_scams() if scam_alert else ""

    system_message = (
        "You are a knowledgeable crypto assistant. "
        "Start with a simple explanation before introducing technical details. "
        "Prioritize user safety by flagging potential scams and referencing real-world incidents."
    )
    
    if scam_alert:
        system_message += f"\n\n🚨 WARNING: This query contains high-risk phrases.\n{live_scam_data}"

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_query}
            ],
            temperature=0.7,
            max_tokens=600
        )

        answer = response.choices[0].message.content
        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
