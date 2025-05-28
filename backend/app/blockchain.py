from web3 import Web3
import json
import os

def get_contract_info():
    # Update path to your ABI and deployed contract address
    abi_path = os.path.join(os.path.dirname(__file__), "../hardhat-project/artifacts/contracts/DataStorage.sol/DataStorage.json")
    with open(abi_path, "r") as f:
        contract_json = json.load(f)
        abi = contract_json['abi']

    # Contract address (replace with actual or read from a file)
    contract_address = "0xe78A0F7E598Cc8b0Bb87894B0F60dD2a88d6a8Ab"

    # Connect to Ganache
    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

    contract = w3.eth.contract(address=contract_address, abi=abi)

    return {
        "contract_address": contract.address,
        "functions": [fn.fn_name for fn in contract.functions]
    }
