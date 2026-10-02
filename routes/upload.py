import os
import random
import pandas as pd
from flask import Blueprint, request, jsonify
from utils.database import verify_token, get_user_id_from_token, save_detection
from services.ml_service import predict, is_ready, get_feature_columns
from services.alert_service import send_alert
from blockchain.blockchain import log_intrusion

upload_bp = Blueprint("upload", __name__)

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "uploads")

def auth_required(request):
    token = request.headers.get("Authorization")
    return verify_token(token)

@upload_bp.route("/api/upload/analyze", methods=["POST"])
def analyze_csv():
    if not auth_required(request):
        return jsonify({"success": False, "message": "Unauthorized"}), 401
    if not is_ready():
        return jsonify({"success": False, "message": "ML model not loaded"}), 500
    if "file" not in request.files:
        return jsonify({"success": False, "message": "No file provided"}), 400

    token = request.headers.get("Authorization")
    user_id = get_user_id_from_token(token)

    file = request.files["file"]
    if not file.filename.endswith(".csv"):
        return jsonify({"success": False, "message": "Only CSV files accepted"}), 400

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    filepath = os.path.join(UPLOAD_DIR, file.filename)
    file.save(filepath)

    try:
        df = pd.read_csv(filepath)
        feature_cols = get_feature_columns()
        missing = [c for c in feature_cols if c not in df.columns]
        if missing:
            return jsonify({"success": False, "message": f"Missing columns: {missing}"}), 400

        results = []
        attacks = 0
        for _, row in df.iterrows():
            features = row[feature_cols].values.astype(float).tolist()
            ip_address = f"{random.randint(1,254)}.{random.randint(0,254)}.{random.randint(0,254)}.{random.randint(1,254)}"
            binary_proba, is_attack, attack_type, confidence = predict(features)
            tx_hash = ""
            if is_attack:
                attacks += 1
                ok, tx_hash = log_intrusion(attack_type, features, binary_proba, ip_address)
                send_alert(binary_proba, ip_address, tx_hash)
            save_detection(user_id, ip_address, binary_proba, is_attack, attack_type, source="upload", tx_hash=tx_hash)
            results.append({
                "ip": ip_address,
                "score": round(binary_proba, 4),
                "is_attack": is_attack,
                "attack_type": attack_type,
                "confidence": round(confidence, 4),
                "tx_hash": tx_hash
            })

        return jsonify({
            "success": True,
            "total": len(results),
            "attacks": attacks,
            "normal": len(results) - attacks,
            "results": results
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500