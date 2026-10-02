import json
import os
from solcx import compile_source, install_solc
from web3 import Web3
from config import GANACHE_URL

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.py")
SOL_PATH = os.path.join(os.path.dirname(__file__), "blockchain", "contract", "Intrusion.sol")

def read_contract():
    with open(SOL_PATH, "r") as f:
        return f.read()

def update_config(address, abi):
    with open(CONFIG_PATH, "r") as f:
        content = f.read()

    abi_json_str = json.dumps(abi)

    lines = content.splitlines()
    new_lines = []
    for line in lines:
        if line.startswith("CONTRACT_ADDRESS"):
            new_lines.append(f'CONTRACT_ADDRESS = "{address}"')
        elif line.startswith("CONTRACT_ABI"):
            new_lines.append(f'CONTRACT_ABI = json.loads({repr(abi_json_str)})')
        else:
            new_lines.append(line)

    with open(CONFIG_PATH, "w") as f:
        f.write("\n".join(new_lines))

    print(f"[CONFIG] Updated config.py with contract address: {address}")

def deploy():
    print("[DEPLOY] Connecting to Ganache...")
    w3 = Web3(Web3.HTTPProvider(GANACHE_URL))

    if not w3.is_connected():
        print("[ERROR] Cannot connect to Ganache. Make sure Ganache is running on", GANACHE_URL)
        return

    print(f"[DEPLOY] Connected: {w3.client_version}")

    print("[DEPLOY] Installing solc compiler...")
    install_solc("0.8.0")

    print("[DEPLOY] Compiling Intrusion.sol...")
    source = read_contract()
    compiled = compile_source(source, output_values=["abi", "bin"], solc_version="0.8.0")
    contract_id, contract_interface = next(iter(compiled.items()))

    abi = contract_interface["abi"]
    bytecode = contract_interface["bin"]

    deployer = w3.eth.accounts[0]
    w3.eth.default_account = deployer

    print(f"[DEPLOY] Deploying from account: {deployer}")

    contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = contract.constructor().transact({"from": deployer, "gas": 3000000})
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    address = receipt.contractAddress
    print(f"[DEPLOY] Contract deployed at: {address}")
    print(f"[DEPLOY] Transaction hash: {receipt.transactionHash.hex()}")

    update_config(address, abi)
    print("[DEPLOY] Done. You can now run: python app.py")

if __name__ == "__main__":
    deploy()