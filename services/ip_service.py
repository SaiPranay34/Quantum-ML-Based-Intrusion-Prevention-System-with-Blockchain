from utils.database import add_blocked_ip, remove_blocked_ip, get_blocked_ips, is_ip_blocked

def block_ip(user_id, ip_address, reason=""):
    if is_ip_blocked(user_id, ip_address):
        return False, "IP already blocked"
    result = add_blocked_ip(user_id, ip_address, reason)
    if result:
        return True, "IP blocked successfully"
    return False, "Failed to block IP"

def unblock_ip(user_id, ip_address):
    if not is_ip_blocked(user_id, ip_address):
        return False, "IP not found in blocked list"
    remove_blocked_ip(user_id, ip_address)
    return True, "IP unblocked successfully"

def list_blocked(user_id):
    return get_blocked_ips(user_id)

def check_blocked(user_id, ip_address):
    return is_ip_blocked(user_id, ip_address)