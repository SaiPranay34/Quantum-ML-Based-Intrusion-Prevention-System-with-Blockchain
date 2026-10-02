from flask import Flask
from flask_cors import CORS
from utils.database import init_db
from services.ml_service import load_model
from routes.auth import auth_bp
from routes.monitor import monitor_bp
from routes.ledger import ledger_bp
from routes.upload import upload_bp
from routes.reports import reports_bp
from routes.settings import settings_bp
from routes.blocked_ips import blocked_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(auth_bp)
app.register_blueprint(monitor_bp)
app.register_blueprint(ledger_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(reports_bp)
app.register_blueprint(settings_bp)
app.register_blueprint(blocked_bp)

if __name__ == "__main__":
    init_db()
    load_model()
    app.run(host="0.0.0.0", port=5000, debug=True)