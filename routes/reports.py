import os
import csv
from datetime import datetime
from flask import Blueprint, request, jsonify, send_from_directory
from utils.database import verify_token, get_user_id_from_token, get_detections, get_dashboard_stats, save_report, get_reports

reports_bp = Blueprint("reports", __name__)

REPORTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "reports")

def auth_required(request):
    token = request.headers.get("Authorization")
    return verify_token(token)

@reports_bp.route("/api/reports/generate", methods=["POST"])
def generate_report():
    if not auth_required(request):
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    token = request.headers.get("Authorization")
    user_id = get_user_id_from_token(token)

    os.makedirs(REPORTS_DIR, exist_ok=True)

    stats = get_dashboard_stats(user_id)
    detections = get_detections(user_id, limit=10000)

    total = stats["total_requests"]
    attacks = stats["total_attacks"]
    normal = stats["total_normal"]

    filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    filepath = os.path.join(REPORTS_DIR, filename)

    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "timestamp", "ip_address", "score", "is_attack", "attack_type", "source", "tx_hash"])
        for d in detections:
            writer.writerow([
                d["id"], d["timestamp"], d["ip_address"],
                d["score"], d["is_attack"], d.get("attack_type", ""),
                d["source"], d["tx_hash"]
            ])

    accuracy = round((normal / total * 100) if total > 0 else 0, 2)
    save_report(user_id, total, attacks, accuracy, filename)

    return jsonify({
        "success": True,
        "filename": filename,
        "total": total,
        "attacks": attacks,
        "normal": normal
    })

@reports_bp.route("/api/reports", methods=["GET"])
def list_reports():
    if not auth_required(request):
        return jsonify({"success": False, "message": "Unauthorized"}), 401
    token = request.headers.get("Authorization")
    user_id = get_user_id_from_token(token)
    reports = get_reports(user_id)
    return jsonify({"success": True, "reports": reports})

@reports_bp.route("/api/reports/download/<filename>", methods=["GET"])
def download_report(filename):
    token = request.args.get("token")
    if not verify_token(token):
        return jsonify({"success": False, "message": "Unauthorized"}), 401
    return send_from_directory(REPORTS_DIR, filename, as_attachment=True)