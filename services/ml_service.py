import numpy as np
import pandas as pd
import joblib
from config import (
    ML_SCALER, ML_PCA, ML_QUANTUM_TRANSFORMER,
    ML_BINARY_MODEL, ML_MULTI_MODEL, ML_LABEL_ENCODER, ML_METRICS
)

FEATURE_COLUMNS = [
    "flow_duration", "Header_Length", "Protocol Type", "Duration",
    "Rate", "Srate", "Drate", "fin_flag_number", "syn_flag_number",
    "rst_flag_number", "psh_flag_number", "ack_flag_number", "ece_flag_number",
    "cwr_flag_number", "ack_count", "syn_count", "fin_count", "urg_count",
    "rst_count", "HTTP", "HTTPS", "DNS", "Telnet", "SMTP", "SSH", "IRC",
    "TCP", "UDP", "DHCP", "ARP", "ICMP", "IPv", "LLC", "Tot sum",
    "Min", "Max", "AVG", "Std", "Tot size", "IAT", "Number",
    "Magnitue", "Radius", "Covariance", "Variance", "Weight"
]

_scaler = None
_pca = None
_quantum_transformer = None
_binary_model = None
_multi_model = None
_label_encoder = None
_metrics = None
_ready = False

def load_model():
    global _scaler, _pca, _quantum_transformer, _binary_model, _multi_model, _label_encoder, _metrics, _ready
    try:
        _scaler = joblib.load(ML_SCALER)
        _pca = joblib.load(ML_PCA)
        _quantum_transformer = joblib.load(ML_QUANTUM_TRANSFORMER)
        _binary_model = joblib.load(ML_BINARY_MODEL)
        _multi_model = joblib.load(ML_MULTI_MODEL)
        _label_encoder = joblib.load(ML_LABEL_ENCODER)
        _metrics = joblib.load(ML_METRICS)
        _ready = True
        print("[ML] All models loaded successfully")
        print(f"[ML] Classes: {list(_label_encoder.classes_)}")
    except Exception as e:
        print(f"[ML] Failed to load models: {e}")
        _ready = False

def is_ready():
    return _ready

def preprocess(row_values):
    x = np.array(row_values).reshape(1, -1)
    x_scaled = _scaler.transform(x)
    x_pca = _pca.transform(x_scaled)
    x_qe = _quantum_transformer.transform(x_pca)
    return x_qe

def predict(row_values):
    if not _ready:
        raise RuntimeError("ML models not loaded")
    x_qe = preprocess(row_values)
    binary_pred = int(_binary_model.predict(x_qe)[0])
    binary_proba = float(_binary_model.predict_proba(x_qe)[0][1])
    multi_pred = int(_multi_model.predict(x_qe)[0])
    multi_proba = _multi_model.predict_proba(x_qe)[0]
    attack_type = _label_encoder.inverse_transform([multi_pred])[0]
    confidence = float(multi_proba.max())
    is_attack = binary_pred == 1
    return binary_proba, is_attack, attack_type, confidence

def get_feature_columns():
    return FEATURE_COLUMNS

def get_label_encoder():
    return _label_encoder

def get_metrics():
    return _metrics