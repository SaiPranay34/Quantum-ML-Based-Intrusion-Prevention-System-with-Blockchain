import sqlite3
import hashlib
import secrets
from config import DB_PATH


def get_conn():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_conn()
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            token TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS smtp_config (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            sender_email TEXT NOT NULL,
            sender_password TEXT NOT NULL,
            recipient_email TEXT NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS blocked_ips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            ip_address TEXT NOT NULL,
            reason TEXT,
            blocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, ip_address)
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS detections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ip_address TEXT,
            score REAL NOT NULL,
            is_attack INTEGER NOT NULL,
            attack_type TEXT,
            source TEXT,
            tx_hash TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total_requests INTEGER,
            total_attacks INTEGER,
            accuracy REAL,
            filename TEXT
        )
    ''')

    conn.commit()
    conn.close()


def get_user_id_from_token(token):
    if not token:
        return None
    conn = get_conn()
    c = conn.cursor()
    c.execute('SELECT id FROM users WHERE token = ?', (token,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None


def register_user(username, email, password):
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    conn = get_conn()
    c = conn.cursor()
    try:
        c.execute(
            'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
            (username, email, password_hash)
        )
        conn.commit()
        return True, "Registered successfully"
    except sqlite3.IntegrityError as e:
        if "username" in str(e):
            return False, "Username already exists"
        return False, "Email already exists"
    finally:
        conn.close()


def login_user(username, password):
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        'SELECT id FROM users WHERE username = ? AND password_hash = ?',
        (username, password_hash)
    )
    user = c.fetchone()
    if user:
        token = secrets.token_hex(32)
        c.execute('UPDATE users SET token = ? WHERE id = ?', (token, user[0]))
        conn.commit()
        conn.close()
        return True, token
    conn.close()
    return False, "Invalid credentials"


def verify_token(token):
    if not token:
        return False
    conn = get_conn()
    c = conn.cursor()
    c.execute('SELECT id FROM users WHERE token = ?', (token,))
    user = c.fetchone()
    conn.close()
    return bool(user)


def logout_user(token):
    conn = get_conn()
    c = conn.cursor()
    c.execute('UPDATE users SET token = NULL WHERE token = ?', (token,))
    conn.commit()
    conn.close()


def save_smtp_config(user_id, sender_email, sender_password, recipient_email):
    conn = get_conn()
    c = conn.cursor()
    c.execute('DELETE FROM smtp_config WHERE user_id = ?', (user_id,))
    c.execute(
        'INSERT INTO smtp_config (user_id, sender_email, sender_password, recipient_email) VALUES (?, ?, ?, ?)',
        (user_id, sender_email, sender_password, recipient_email)
    )
    conn.commit()
    conn.close()


def get_smtp_config(user_id=None):
    conn = get_conn()
    c = conn.cursor()
    if user_id:
        c.execute('SELECT sender_email, sender_password, recipient_email FROM smtp_config WHERE user_id = ? LIMIT 1', (user_id,))
    else:
        c.execute('SELECT sender_email, sender_password, recipient_email FROM smtp_config LIMIT 1')
    row = c.fetchone()
    conn.close()
    if row:
        return {"sender_email": row[0], "sender_password": row[1], "recipient_email": row[2]}
    return None


def add_blocked_ip(user_id, ip_address, reason=""):
    conn = get_conn()
    c = conn.cursor()
    try:
        c.execute(
            'INSERT INTO blocked_ips (user_id, ip_address, reason) VALUES (?, ?, ?)',
            (user_id, ip_address, reason)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def remove_blocked_ip(user_id, ip_address):
    conn = get_conn()
    c = conn.cursor()
    c.execute('DELETE FROM blocked_ips WHERE user_id = ? AND ip_address = ?', (user_id, ip_address))
    conn.commit()
    conn.close()


def get_blocked_ips(user_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute('SELECT id, ip_address, reason, blocked_at FROM blocked_ips WHERE user_id = ? ORDER BY blocked_at DESC', (user_id,))
    rows = c.fetchall()
    conn.close()
    return [{"id": r[0], "ip_address": r[1], "reason": r[2], "blocked_at": r[3]} for r in rows]


def is_ip_blocked(user_id, ip_address):
    conn = get_conn()
    c = conn.cursor()
    c.execute('SELECT id FROM blocked_ips WHERE user_id = ? AND ip_address = ?', (user_id, ip_address))
    row = c.fetchone()
    conn.close()
    return bool(row)


def save_detection(user_id, ip_address, score, is_attack, attack_type="", source="live", tx_hash=""):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        'INSERT INTO detections (user_id, ip_address, score, is_attack, attack_type, source, tx_hash) VALUES (?, ?, ?, ?, ?, ?, ?)',
        (user_id, ip_address, score, int(is_attack), attack_type, source, tx_hash)
    )
    conn.commit()
    conn.close()


def get_detections(user_id, limit=100):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        'SELECT id, timestamp, ip_address, score, is_attack, attack_type, source, tx_hash FROM detections WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?',
        (user_id, limit)
    )
    rows = c.fetchall()
    conn.close()
    return [
        {
            "id": r[0], "timestamp": r[1], "ip_address": r[2],
            "score": r[3], "is_attack": bool(r[4]), "attack_type": r[5],
            "source": r[6], "tx_hash": r[7]
        }
        for r in rows
    ]


def get_dashboard_stats(user_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM detections WHERE user_id = ?', (user_id,))
    total = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM detections WHERE user_id = ? AND is_attack = 1', (user_id,))
    attacks = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM blocked_ips WHERE user_id = ?', (user_id,))
    blocked = c.fetchone()[0]
    conn.close()
    normal = total - attacks
    return {
        "total_requests": total,
        "total_attacks": attacks,
        "total_normal": normal,
        "blocked_ips": blocked
    }


def save_report(user_id, total_requests, total_attacks, accuracy, filename):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        'INSERT INTO reports (user_id, total_requests, total_attacks, accuracy, filename) VALUES (?, ?, ?, ?, ?)',
        (user_id, total_requests, total_attacks, accuracy, filename)
    )
    conn.commit()
    conn.close()


def get_reports(user_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        'SELECT id, generated_at, total_requests, total_attacks, accuracy, filename FROM reports WHERE user_id = ? ORDER BY generated_at DESC',
        (user_id,)
    )
    rows = c.fetchall()
    conn.close()
    return [
        {
            "id": r[0], "generated_at": r[1], "total_requests": r[2],
            "total_attacks": r[3], "accuracy": r[4], "filename": r[5]
        }
        for r in rows
    ]