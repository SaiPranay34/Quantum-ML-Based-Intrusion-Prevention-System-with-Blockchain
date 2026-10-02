from flask import Blueprint, request, jsonify
from utils.database import verify_token, get_user_id_from_token, save_smtp_config, get_smtp_config

settings_bp = Blueprint("settings", __name__)

def auth_required(request):
    token = request.headers.get("Authorization")
    return verify_token(token)

@settings_bp.route("/api/settings/smtp", methods=["GET"])
def get_settings():
    if not auth_required(request):
        return jsonify({"success": False, "message": "Unauthorized"}), 401
    token = request.headers.get("Authorization")
    user_id = get_user_id_from_token(token)
    config = get_smtp_config(user_id)
    if config:
        return jsonify({
            "success": True,
            "sender_email": config["sender_email"],
            "recipient_email": config["recipient_email"]
        })
    return jsonify({"success": True, "sender_email": "", "recipient_email": ""})

@settings_bp.route("/api/settings/smtp", methods=["POST"])
def save_settings():
    if not auth_required(request):
        return jsonify({"success": False, "message": "Unauthorized"}), 401
    token = request.headers.get("Authorization")
    user_id = get_user_id_from_token(token)
    data = request.json
    sender_email = data.get("sender_email", "").strip()
    sender_password = data.get("sender_password", "").strip()
    recipient_email = data.get("recipient_email", "").strip()
    if not sender_email or not sender_password or not recipient_email:
        return jsonify({"success": False, "message": "All fields required"}), 400
    save_smtp_config(user_id, sender_email, sender_password, recipient_email)
    return jsonify({"success": True, "message": "SMTP settings saved"})