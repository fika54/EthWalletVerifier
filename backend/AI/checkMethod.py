import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

#import APIcall as API
#import FinalAI
from backend.AI import APIcall as API
from backend.AI import FinalAI


def checkWallet(walletAddress, API_KEY):
    print("Checking wallet...")
    # Fetch and display transaction data
    df = API.runVerification(walletAddress, API_KEY)

    print(df)

    print("Testing the data...")

    # Run the AI model on the data
    result = FinalAI.verifWallet(df)

    return result

# Test the function
#results = checkWallet('0x8901158D31cF020B03672BbFFEb7688f09Cf5852')
#print("class: ",results.get('class'), "confidence: ", results.get('confidence'))