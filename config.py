import os
import json

GANACHE_URL = "http://127.0.0.1:7545"

CONTRACT_ADDRESS = "0xD2e703232Aab2177B1c39694Aa63A378Cad1b0B6"
CONTRACT_ABI = json.loads('[{"inputs": [], "stateMutability": "nonpayable", "type": "constructor"}, {"anonymous": false, "inputs": [{"indexed": true, "internalType": "uint256", "name": "id", "type": "uint256"}, {"indexed": false, "internalType": "string", "name": "attackType", "type": "string"}, {"indexed": false, "internalType": "uint256", "name": "confidence", "type": "uint256"}], "name": "IntrusionLogged", "type": "event"}, {"inputs": [], "name": "getAllLogs", "outputs": [{"components": [{"internalType": "uint256", "name": "id", "type": "uint256"}, {"internalType": "uint256", "name": "timestamp", "type": "uint256"}, {"internalType": "string", "name": "attackType", "type": "string"}, {"internalType": "string", "name": "dataHash", "type": "string"}, {"internalType": "uint256", "name": "confidence", "type": "uint256"}, {"internalType": "string", "name": "ipAddress", "type": "string"}], "internalType": "struct Intrusion.Log[]", "name": "", "type": "tuple[]"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "index", "type": "uint256"}], "name": "getLog", "outputs": [{"components": [{"internalType": "uint256", "name": "id", "type": "uint256"}, {"internalType": "uint256", "name": "timestamp", "type": "uint256"}, {"internalType": "string", "name": "attackType", "type": "string"}, {"internalType": "string", "name": "dataHash", "type": "string"}, {"internalType": "uint256", "name": "confidence", "type": "uint256"}, {"internalType": "string", "name": "ipAddress", "type": "string"}], "internalType": "struct Intrusion.Log", "name": "", "type": "tuple"}], "stateMutability": "view", "type": "function"}, {"inputs": [], "name": "getLogsCount", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "string", "name": "_attackType", "type": "string"}, {"internalType": "string", "name": "_dataHash", "type": "string"}, {"internalType": "uint256", "name": "_confidence", "type": "uint256"}, {"internalType": "string", "name": "_ipAddress", "type": "string"}], "name": "logIntrusion", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [], "name": "owner", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "stateMutability": "view", "type": "function"}]')

DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587

ML_SCALER = os.path.join(os.path.dirname(__file__), "scaler_standard.pkl")
ML_PCA = os.path.join(os.path.dirname(__file__), "pca_quantum_reducer.pkl")
ML_QUANTUM_TRANSFORMER = os.path.join(os.path.dirname(__file__), "quantum_feature_transformer.pkl")
ML_BINARY_MODEL = os.path.join(os.path.dirname(__file__), "binary_model.pkl")
ML_MULTI_MODEL = os.path.join(os.path.dirname(__file__), "multi_model.pkl")
ML_LABEL_ENCODER = os.path.join(os.path.dirname(__file__), "label_encoder.pkl")
ML_METRICS = os.path.join(os.path.dirname(__file__), "model_metrics.pkl")

ATTACK_THRESHOLD = 0.5

SECRET_KEY = os.urandom(32).hex()