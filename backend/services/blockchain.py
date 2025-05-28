from web3 import Web3
import json
import os

# Load contract ABI and address
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONTRACT_JSON_PATH = os.path.join(BASE_DIR, '../blockchain/build/DataStorage.json')

with open(CONTRACT_JSON_PATH, 'r') as f:
    contract_json = json.load(f)
    contract_abi = contract_json['abi']

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

if not w3.is_connected():
    raise Exception('Web3 is not connected')

CONTRACT_ADDRESS = Web3.to_checksum_address('0xe78A0F7E598Cc8b0Bb87894B0F60dD2a88d6a8Ab')

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)

def send_sensor_data(temperature, acceleration):
    # This is a stub. Implement your blockchain send logic here.
    # For example, build and send a transaction to your contract.
    tx_hash = 'dummy_tx_hash_for_now'
    return tx_hash
