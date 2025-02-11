# backend/services/blockchain_service.py

import requests
from utils.config import FLARE_FDC_URL

def check_wallet_risk(wallet_address):
    """
    Checks if 'wallet_address' is flagged by Flare FDC or other sources.
    Returns a dict: { "wallet_address", "flagged", "risk_level", "reason" }
    """
    flagged = False
    reason = "No known reports."

    try:
        # >>> FILL HERE (Potentially) <<<
        # The actual endpoint might differ. Adjust this to match the real Flare API URL.
        url = f"{FLARE_FDC_URL}/{wallet_address}"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            flagged = data.get('flagged', False)
            reason = data.get('reason', reason)
        else:
            reason = f"Failed to retrieve data from FDC (status: {resp.status_code})."
    except Exception as e:
        reason = f"Error calling FDC: {e}"

    if flagged:
        risk_level = "High"
    else:
        risk_level = "Low"

    return {
        "wallet_address": wallet_address,
        "flagged": flagged,
        "risk_level": risk_level,
        "reason": reason
    }
