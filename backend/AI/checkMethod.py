import os
import sys

# Set the project root directory and add it to the system path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

# Uncomment these lines if you want to test the code in this file
# import APIcall as API
# import FinalAI

# Comment these lines if you want to test the code in this file
from backend.AI import APIcall as API
from backend.AI import FinalAI

def checkWallet(walletAddress, API_KEY):
    """
    Checks the given wallet address by fetching transaction data
    and running it through an AI verification model.
    
    :param walletAddress: str: The wallet address to check
    :param API_KEY: str: API key for authentication
    :return: Result from the AI model
    """
    print("Checking wallet...")
    
    # Fetch and display transaction data
    df = API.runVerification(walletAddress, API_KEY)
    print(df)
    
    print("Testing the data...")
    
    # Run the AI model on the fetched data
    result = FinalAI.verifWallet(df)
    
    return result
