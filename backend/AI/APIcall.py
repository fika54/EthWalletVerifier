import requests
import time
import pandas as pd
from moralis import evm_api

def fetch_transactions(address, cursor, API_KEY):
    """
    Fetch transaction history for a given wallet address.
    :param address: str: Target wallet address
    :param after: str: Cursor for pagination
    :return: dict: Transaction history data
    """
    
    params = {
    "address": address,
    "order": "DESC",
    "chain": "eth",
    "cursor": cursor,
    }


    result = evm_api.transaction.get_wallet_transactions(
    api_key = API_KEY,
    params = params,
    )

    return result


def parse_transactions(data, df, address):

    print(data['page'])   

    for txn in data["result"]:

        txn["block_number"] = int(txn["block_number"])
        txn["from_address"] = txn["from_address"].lower()
        txn["to_address"] = txn["to_address"].lower()
        address = address.lower()

        df.loc[0, 'total_txs'] += 1

        if df.loc[0, 'first_block_appeared_in'] == 0 or txn["block_number"] < df.loc[0, 'first_block_appeared_in']:
            df.loc[0, 'first_block_appeared_in'] = txn["block_number"]

        if txn["block_number"] > df.loc[0, 'last_block_appeared_in']:
            df.loc[0, 'last_block_appeared_in'] = txn["block_number"]

        if txn['from_address'] == address:
            df.loc[0, 'num_txs_as_sender'] += 1
            if df.loc[0, 'first_sent_block'] == 0 or txn["block_number"] < df.loc[0, 'first_sent_block']:
                df.loc[0, 'first_sent_block'] = txn["block_number"]

        if txn['to_address']== address:
            df.loc[0, 'num_txs_as receiver'] += 1
            if df.loc[0, 'first_received_block'] == 0 or txn["block_number"] < df.loc[0, 'first_received_block']:
                df.loc[0, 'first_received_block'] = txn["block_number"]

    df.loc[0, 'lifetime_in_blocks'] = df.loc[0, 'last_block_appeared_in'] - df.loc[0, 'first_block_appeared_in']


def runVerification(walletAddress, API_KEY):
    # Fetch and display transaction data
    data = fetch_transactions(walletAddress,"", API_KEY)

    df = pd.DataFrame(columns=['num_txs_as_sender', 'num_txs_as receiver', 'first_block_appeared_in', 
                              'last_block_appeared_in', 'lifetime_in_blocks', 'total_txs', 
                               'first_sent_block', 'first_received_block'], index=[0])
    
    df.loc[:] = 0

    if data:
        parse_transactions(data, df, walletAddress)
        # Handle pagination if there are more results
        cursor = data["cursor"]
        while cursor != None and cursor != "":  
            data = fetch_transactions(walletAddress, cursor, API_KEY)
            cursor = data["cursor"]
            if data:
                parse_transactions(data, df, walletAddress)
            else:
                break

    return df

#df = runVerification('0xD3a22590f8243f8E83Ac230D1842C9Af0404C4A1')

#print(df)



