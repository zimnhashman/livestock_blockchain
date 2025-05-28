import os
import json
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()  # <-- Add this line

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONTRACT_JSON_PATH = os.path.join(BASE_DIR, 'build', 'DataStorage.json')

with open(CONTRACT_JSON_PATH, 'r') as f:
    contract_json = json.load(f)
    contract_abi = contract_json['abi']

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

if not w3.is_connected():
    raise Exception('Web3 is not connected')

CONTRACT_ADDRESS = Web3.to_checksum_address('0xe78a0f7e598cc8b0bb87894b0f60dd2a88d6a8ab')

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)

FARMER_ADDRESS = os.getenv('FARMER_ADDRESS')
FARMER_PRIVATE_KEY = os.getenv('FARMER_PRIVATE_KEY')

if not FARMER_ADDRESS or not FARMER_PRIVATE_KEY:
    raise Exception("Please set FARMER_ADDRESS and FARMER_PRIVATE_KEY environment variables")
