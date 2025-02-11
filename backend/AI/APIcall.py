import requests
import time
import pandas as pd
from moralis import evm_api

def fetch_transactions(address, cursor, API_KEY):
    """
    Fetch transaction history for a given wallet address.
    :param address: str: Target wallet address
    :param cursor: str: Cursor for pagination
    :param API_KEY: str: API key for authentication
    :return: dict: Transaction history data
    """
    
    params = {
        "address": address,
        "order": "DESC",  # Fetch transactions in descending order
        "chain": "eth",   # Specify Ethereum blockchain
        "cursor": cursor,  # Pagination cursor
    }

    # Call Moralis API to get wallet transactions
    result = evm_api.transaction.get_wallet_transactions(
        api_key=API_KEY,
        params=params,
    )
    
    return result

def parse_transactions(data, df, address):
    """
    Parse transaction data and update the DataFrame with relevant details.
    :param data: dict: Transaction data from API
    :param df: DataFrame: Data structure to store processed transaction information
    :param address: str: Target wallet address
    """
    
    print(data['page'])  # Print current page number for debugging
    
    for txn in data["result"]:
        # Convert block number to integer for consistency
        txn["block_number"] = int(txn["block_number"])
        
        # Convert addresses to lowercase for uniformity
        txn["from_address"] = txn["from_address"].lower()
        txn["to_address"] = txn["to_address"].lower()
        address = address.lower()
        
        # Increment total transaction count
        df.loc[0, 'total_txs'] += 1
        
        # Determine the first block the wallet appeared in
        if df.loc[0, 'first_block_appeared_in'] == 0 or txn["block_number"] < df.loc[0, 'first_block_appeared_in']:
            df.loc[0, 'first_block_appeared_in'] = txn["block_number"]
        
        # Determine the last block the wallet appeared in
        if txn["block_number"] > df.loc[0, 'last_block_appeared_in']:
            df.loc[0, 'last_block_appeared_in'] = txn["block_number"]
        
        # Count transactions where the wallet is the sender
        if txn['from_address'] == address:
            df.loc[0, 'num_txs_as_sender'] += 1
            if df.loc[0, 'first_sent_block'] == 0 or txn["block_number"] < df.loc[0, 'first_sent_block']:
                df.loc[0, 'first_sent_block'] = txn["block_number"]
        
        # Count transactions where the wallet is the receiver
        if txn['to_address'] == address:
            df.loc[0, 'num_txs_as receiver'] += 1
            if df.loc[0, 'first_received_block'] == 0 or txn["block_number"] < df.loc[0, 'first_received_block']:
                df.loc[0, 'first_received_block'] = txn["block_number"]
    
    # Calculate wallet's lifetime in blocks
    df.loc[0, 'lifetime_in_blocks'] = df.loc[0, 'last_block_appeared_in'] - df.loc[0, 'first_block_appeared_in']

def runVerification(walletAddress, API_KEY):
    """
    Run verification process for a given wallet address.
    :param walletAddress: str: Wallet address to verify
    :param API_KEY: str: API key for authentication
    :return: DataFrame: Processed transaction summary
    """
    
    # Fetch initial transaction data
    data = fetch_transactions(walletAddress, "", API_KEY)
    
    # Initialize DataFrame to store transaction details
    df = pd.DataFrame(columns=['num_txs_as_sender', 'num_txs_as receiver', 'first_block_appeared_in', 
                               'last_block_appeared_in', 'lifetime_in_blocks', 'total_txs', 
                               'first_sent_block', 'first_received_block'], index=[0])
    
    df.loc[:] = 0  # Initialize all values to zero
    
    if data:
        parse_transactions(data, df, walletAddress)
        
        # Handle pagination if there are more results
        cursor = data["cursor"]
        while cursor is not None and cursor != "":  
            data = fetch_transactions(walletAddress, cursor, API_KEY)
            cursor = data["cursor"]
            if data:
                parse_transactions(data, df, walletAddress)
            else:
                break
    
    return df
