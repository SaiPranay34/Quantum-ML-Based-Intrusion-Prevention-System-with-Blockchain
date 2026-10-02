from flask import Blueprint, request, jsonify
from utils.database import verify_token, get_user_id_from_token
from services.ip_service import block_ip, unblock_ip, list_blocked

blocked_bp = Blueprint("blocked", __name__)

def auth_required(request):
    token = request.headers.get("Authorization")
    return verify_token(token)

@blocked_bp.route("/api/blocked", methods=["GET"])
def get_blocked():
    if not auth_required(request):
        return jsonify({"success": False, "message": "Unauthorized"}), 401
    token = request.headers.get("Authorization")
    user_id = get_user_id_from_token(token)
    ips = list_blocked(user_id)
    return jsonify({"success": True, "blocked_ips": ips})

@blocked_bp.route("/api/blocked", methods=["POST"])
def block():
    if not auth_required(request):
        return jsonify({"success": False, "message": "Unauthorized"}), 401
    token = request.headers.get("Authorization")
    user_id = get_user_id_from_token(token)
    data = request.json
    ip = data.get("ip_address", "").strip()
    reason = data.get("reason", "").strip()
    if not ip:
        return jsonify({"success": False, "message": "IP address required"}), 400
    success, message = block_ip(user_id, ip, reason)
    if success:
        return jsonify({"success": True, "message": message})
    return jsonify({"success": False, "message": message}), 409

@blocked_bp.route("/api/blocked/<ip_address>", methods=["DELETE"])
def unblock(ip_address):
    if not auth_required(request):
        return jsonify({"success": False, "message": "Unauthorized"}), 401
    token = request.headers.get("Authorization")
    user_id = get_user_id_from_token(token)
    success, message = unblock_ip(user_id, ip_address)
    if success:
        return jsonify({"success": True, "message": message})
    return jsonify({"success": False, "message": message}), 404