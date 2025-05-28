from web3 import Web3
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

# Load contract ABI
contract_path = os.path.join(os.path.dirname(__file__), 'build', 'DataStorage.json')
with open(contract_path) as f:
    contract_json = json.load(f)

contract_abi = contract_json['abi']

# Get contract address and private key from .env
contract_address = os.getenv("CONTRACT_ADDRESS")
private_key = os.getenv("PRIVATE_KEY")

if not contract_address or not private_key:
    raise Exception("Missing CONTRACT_ADDRESS or PRIVATE_KEY in .env")

contract = w3.eth.contract(
    address=w3.to_checksum_address(contract_address),
    abi=contract_abi
)

def send_sensor_data(temperature: int, acceleration: int) -> str:
    account = w3.eth.account.from_key(private_key).address

    tx = contract.functions.submitData(temperature, acceleration).build_transaction({
        'from': account,
        'nonce': w3.eth.get_transaction_count(account),
        'gas': 2000000,
        'gasPrice': w3.to_wei('20', 'gwei')
    })

    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    return w3.to_hex(tx_hash)
