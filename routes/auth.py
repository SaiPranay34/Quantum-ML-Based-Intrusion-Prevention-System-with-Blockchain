from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from utils.database import register_user, login_user, verify_token, logout_user

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/")
def index():
    return render_template("index.html")

@auth_bp.route("/signup", methods=["GET"])
def signup_page():
    return render_template("signup.html")

@auth_bp.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")

@auth_bp.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@auth_bp.route("/api/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()
    if not username or not email or not password:
        return jsonify({"success": False, "message": "All fields required"}), 400
    success, message = register_user(username, email, password)
    if success:
        return jsonify({"success": True, "message": message})
    return jsonify({"success": False, "message": message}), 409

@auth_bp.route("/api/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()
    if not username or not password:
        return jsonify({"success": False, "message": "All fields required"}), 400
    success, result = login_user(username, password)
    if success:
        return jsonify({"success": True, "token": result, "username": username})
    return jsonify({"success": False, "message": result}), 401

@auth_bp.route("/api/logout", methods=["POST"])
def logout():
    token = request.headers.get("Authorization")
    logout_user(token)
    return jsonify({"success": True})

@auth_bp.route("/api/verify", methods=["GET"])
def verify():
    token = request.headers.get("Authorization")
    if verify_token(token):
        return jsonify({"success": True})
    return jsonify({"success": False}), 401