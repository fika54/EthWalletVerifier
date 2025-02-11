import streamlit as st
import requests
import time
import random
import string
import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from backend.AI import checkMethod

# -------------------------------------------------------------------------
# Configuration: Must be the very first command!
# -------------------------------------------------------------------------
st.set_page_config(page_title="AI Crypto Guardian", page_icon="🤖", layout="wide")

# -------------------------------------------------------------------------
# Inject an inline SVG with a gradient definition for the arrow fill
# -------------------------------------------------------------------------
st.markdown(
    """
    <svg width="0" height="0" style="position:absolute">
      <defs>
        <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="#FFA500" />  <!-- Orange -->
          <stop offset="50%" stop-color="#FF0000" />  <!-- Red -->
          <stop offset="100%" stop-color="#1E90FF" /> <!-- Blue -->
        </linearGradient>
      </defs>
    </svg>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------------------------------
# Define a function to simulate a fake decryption effect
# -------------------------------------------------------------------------
def simulate_decryption(placeholder, final_text, delay=0.05, iterations=15):
    """
    Simulate a decryption effect by gradually replacing random characters
    with the final text.
    """
    final_chars = list(final_text)
    current = [random.choice(string.ascii_letters + string.digits) if c != " " else " " for c in final_chars]
    for i in range(iterations):
        for j in range(len(final_chars)):
            if random.random() < float(i + 1) / iterations:
                current[j] = final_chars[j]
            else:
                if final_chars[j] != " ":
                    current[j] = random.choice(string.ascii_letters + string.digits)
        placeholder.markdown(" **" + "".join(current) + "**")
        time.sleep(delay)
        time.sleep(delay)
    placeholder.markdown(" **" + final_text + "**")

# -------------------------------------------------------------------------
# Minimal Custom CSS Styling (Neutral Theme, Except Arrow)
# -------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* Basic styling: neutral background and text */
    body {
        font-family: 'Open Sans', sans-serif;
        background: #ffffff;
        color: #000000;
        margin: 0;
        padding: 0;
    }

    /* Header container: centered, with simple padding */
    .header-container {
        text-align: center;
        margin-bottom: 30px;
        padding: 20px;
    }

    /* Chat input container: fixed at the bottom with neutral colors.
       Remains at left: 55px. */
    [data-testid="stChatInput"] {
        position: fixed;
        bottom: 0;
        left: 55px;
        width: calc(100% - 40px);
        max-width: 1600px;
        background-color: #ffffff;
        border-top: 1px solid #ddd;
        padding: 10px 20px;
        border-radius: 20px 20px 0 0;
        box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.1);
        z-index: 1000;
    }
    /* Chat input field: neutral styling.
       The negative left margin shifts the actual text field 10px to the left relative to the container. */
    [data-testid="stChatInput"] input {
        width: 100% !important;
        padding: 10px 15px;
        font-size: 16px;
        border: 1px solid #ddd;
        border-radius: 20px;
        background: #ffffff;
        margin: 0;
        margin-left: -10px;
    }
    [data-testid="stChatInput"] input:focus {
        outline: none;
        border-color: #aaa;
    }
    
    /* --- Arrow Styling ---
       The arrow (submit button icon) is the only colored element.
       Its fill uses the gradient defined in the injected SVG.
       The default transform moves it 20px to the left and 3px upward.
       On hover, it scales up to 1.2× and increases brightness.
    */
    [data-testid="stChatInput"] button {
        margin-right: 5px;
        padding: 5px;
        background: transparent;
        border: none;
        cursor: pointer;
    }
    [data-testid="stChatInput"] button svg {
        transform: translate(-20px, -3px);
        transition: transform 0.3s ease, filter 0.3s ease;
        fill: url(#gradient);
    }
    [data-testid="stChatInput"] button:hover svg {
        transform: translate(-20px, -3px) scale(1.2);
        filter: brightness(1.3);
    }
    
    /* Extra bottom spacing so content isn’t hidden behind the fixed chat input */
    .main {
        padding-bottom: 120px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------------------------------
# Centered Header & Description
# -------------------------------------------------------------------------
st.markdown(
    """
    <div class="header-container">
        <h1>AI Crypto Guardian</h1>
        <p>Protecting & Educating You on Crypto Scams</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------------------------------
# Backend API Base URL
# -------------------------------------------------------------------------
BACKEND_URL = "http://localhost:5001"

# -------------------------------------------------------------------------
# Helper Function for POST Requests
# -------------------------------------------------------------------------
def post_request(endpoint: str, payload: dict, spinner_text: str = "Processing..."):
    """
    Perform a POST request with error handling.
    Returns the JSON response if successful; otherwise, returns None.
    """
    with st.spinner(spinner_text):
        try:
            response = requests.post(endpoint, json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            st.error(f"Error: {e}")
            return None

# -------------------------------------------------------------------------
# Main App Tabs: AI Chat, Scam Detector, Wallet Verification
# -------------------------------------------------------------------------
tab_wallet = st.tabs(["🔗 Wallet Verification"])[0]

# -------------------------------------------------------------------------
# Wallet Verification Tab
# -------------------------------------------------------------------------
with tab_wallet:
    st.header("Wallet Verification")
    st.write("Check if a wallet address is flagged by our systems. (Etherum addresses only)")

    wallet_address = st.text_input("Enter wallet address (e.g., 0xabc123):")
    url = "https://docs.moralis.com/"
    API_KEY = st.text_input("Enter your API Key: (Sign up [here](%s) to get an API key)" % url, type="password")
    if st.button("Verify Wallet", key="verify_wallet"):
        if wallet_address.strip():
            payload = {"wallet_address": wallet_address}
            data = checkMethod.checkWallet(wallet_address,API_KEY)
            if data:
                flagged = data.get("class")

                if (flagged == 1):
                    flagged = True
                else:
                    flagged = False
                    
                risk_level = data.get("confidence")

                if (flagged == True):
                    risk_level = (risk_level) * 100
                else:
                    risk_level = (risk_level) * 100
                reason = data.get("reason", "N/A")
                
                st.write(f"**Wallet:** {wallet_address}")
                st.write(f"**Flagged:** {flagged}")
                st.write(f"**Confidence Level:** {risk_level}")
                st.write(f"**Reason:** {reason}")

                if flagged:
                    st.error("This wallet is considered High Risk!")
                else:
                    st.success("No known flags for this wallet.")
        else:
            st.warning("Please enter a wallet address for verification.")
