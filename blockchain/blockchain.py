import hashlib
import time
from web3 import Web3
from config import GANACHE_URL, CONTRACT_ADDRESS, CONTRACT_ABI

_w3 = None
_contract = None

def get_web3():
    global _w3
    if _w3 is None:
        _w3 = Web3(Web3.HTTPProvider(GANACHE_URL))
    return _w3

def get_contract():
    global _contract
    if _contract is None:
        if not CONTRACT_ADDRESS or not CONTRACT_ABI:
            raise RuntimeError("Contract not deployed. Run python deploy.py first.")
        w3 = get_web3()
        if not w3.is_connected():
            raise RuntimeError(f"Cannot connect to Ganache at {GANACHE_URL}")
        _contract = w3.eth.contract(
            address=Web3.to_checksum_address(CONTRACT_ADDRESS),
            abi=CONTRACT_ABI
        )
    return _contract

def is_connected():
    try:
        return get_web3().is_connected()
    except Exception:
        return False

def log_intrusion(attack_type, raw_data, confidence, ip_address="unknown"):
    try:
        w3 = get_web3()
        contract = get_contract()
        w3.eth.default_account = w3.eth.accounts[0]

        data_hash = hashlib.sha256(str(raw_data).encode()).hexdigest()
        confidence_int = int(confidence * 100)

        tx = contract.functions.logIntrusion(
            attack_type,
            data_hash,
            confidence_int,
            ip_address
        ).transact({"from": w3.eth.accounts[0], "gas": 300000})

        receipt = w3.eth.wait_for_transaction_receipt(tx)
        tx_hash = receipt.transactionHash.hex()
        return True, tx_hash
    except Exception as e:
        return False, str(e)

def get_all_logs():
    try:
        contract = get_contract()
        logs = contract.functions.getAllLogs().call()
        result = []
        for log in logs:
            result.append({
                "id": log[0],
                "timestamp": log[1],
                "attackType": log[2],
                "dataHash": log[3],
                "confidence": log[4],
                "ipAddress": log[5]
            })
        return list(reversed(result))
    except Exception as e:
        return []

def get_logs_count():
    try:
        contract = get_contract()
        return contract.functions.getLogsCount().call()
    except Exception:
        return 0