from flask import Blueprint, request, jsonify
from utils.database import verify_token
from blockchain.blockchain import get_all_logs, get_logs_count, is_connected

ledger_bp = Blueprint("ledger", __name__)

def auth_required(request):
    token = request.headers.get("Authorization")
    return verify_token(token)

@ledger_bp.route("/api/ledger", methods=["GET"])
def get_ledger():
    if not auth_required(request):
        return jsonify({"success": False, "message": "Unauthorized"}), 401
    try:
        logs = get_all_logs()
        count = get_logs_count()
        return jsonify({"success": True, "count": count, "logs": logs})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@ledger_bp.route("/api/ledger/status", methods=["GET"])
def ledger_status():
    if not auth_required(request):
        return jsonify({"success": False, "message": "Unauthorized"}), 401
    connected = is_connected()
    count = get_logs_count() if connected else 0
    return jsonify({"success": True, "connected": connected, "total_logs": count})