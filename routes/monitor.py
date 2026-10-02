import os
import time
import random
import json
import pandas as pd
from flask import Blueprint, request, jsonify, Response
from utils.database import verify_token, get_user_id_from_token, save_detection, get_detections, get_dashboard_stats
from services.ml_service import predict, is_ready, get_feature_columns
from services.alert_service import send_alert
from blockchain.blockchain import log_intrusion

monitor_bp = Blueprint("monitor", __name__)

SIMULATION_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "datasets", "simulation")

def auth_required(request):
    token = request.headers.get("Authorization")
    return verify_token(token)

@monitor_bp.route("/api/monitor/datasets", methods=["GET"])
def list_datasets():
    if not auth_required(request):
        return jsonify({"success": False, "message": "Unauthorized"}), 401
    files = []
    if os.path.exists(SIMULATION_DIR):
        files = [f for f in os.listdir(SIMULATION_DIR) if f.endswith(".csv")]
        files.sort()
    return jsonify({"success": True, "files": files})

@monitor_bp.route("/api/monitor/stream", methods=["GET"])
def stream():
    token = request.args.get("token")
    if not verify_token(token):
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    user_id = get_user_id_from_token(token)
    filename = request.args.get("file")
    if not filename:
        return jsonify({"success": False, "message": "No file specified"}), 400

    filepath = os.path.join(SIMULATION_DIR, filename)
    if not os.path.exists(filepath):
        return jsonify({"success": False, "message": "File not found"}), 404

    def generate():
        df = pd.read_csv(filepath)
        feature_cols = get_feature_columns()
        for _, row in df.iterrows():
            if not is_ready():
                break
            try:
                features = row[feature_cols].values.astype(float).tolist()
                ip_address = f"{random.randint(1,254)}.{random.randint(0,254)}.{random.randint(0,254)}.{random.randint(1,254)}"
                binary_proba, is_attack, attack_type, confidence = predict(features)
                tx_hash = ""
                if is_attack:
                    ok, tx_hash = log_intrusion(attack_type, features, binary_proba, ip_address)
                    send_alert(binary_proba, ip_address, tx_hash)
                save_detection(user_id, ip_address, binary_proba, is_attack, attack_type, source="live", tx_hash=tx_hash)
                data = json.dumps({
                    "ip": ip_address,
                    "score": round(binary_proba, 4),
                    "is_attack": is_attack,
                    "attack_type": attack_type,
                    "confidence": round(confidence, 4),
                    "tx_hash": tx_hash
                })
                yield f"data: {data}\n\n"
                time.sleep(1)
            except Exception as e:
                yield f"data: {{}}\n\n"
                break
        yield "data: {\"done\": true}\n\n"

    return Response(generate(), mimetype="text/event-stream",
                    headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})

@monitor_bp.route("/api/monitor/detections", methods=["GET"])
def detections():
    if not auth_required(request):
        return jsonify({"success": False, "message": "Unauthorized"}), 401
    token = request.headers.get("Authorization")
    user_id = get_user_id_from_token(token)
    limit = request.args.get("limit", 100, type=int)
    data = get_detections(user_id, limit)
    return jsonify({"success": True, "detections": data})

@monitor_bp.route("/api/monitor/stats", methods=["GET"])
def stats():
    if not auth_required(request):
        return jsonify({"success": False, "message": "Unauthorized"}), 401
    token = request.headers.get("Authorization")
    user_id = get_user_id_from_token(token)
    data = get_dashboard_stats(user_id)
    return jsonify({"success": True, "stats": data})