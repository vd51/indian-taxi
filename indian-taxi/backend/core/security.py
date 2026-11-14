import hashlib, hmac, secrets
from datetime import datetime, timedelta, timezone
from backend.core.config import settings

def hash_password(pw: str) -> str:
    salt = secrets.token_hex(16)
    h = hashlib.pbkdf2_hmac('sha256', pw.encode(), salt.encode(), 100000).hex()
    return f"{salt}:{h}"

def verify_password(pw: str, stored: str) -> bool:
    try:
        salt, h = stored.split(":")
        new_h = hashlib.pbkdf2_hmac('sha256', pw.encode(), salt.encode(), 100000).hex()
        return hmac.compare_digest(h, new_h)
    except: return False

def hash_otp(challenge_id: str, otp: str) -> str:
    return hashlib.sha256(f"{challenge_id}:{otp}:{settings.SECRET_KEY}".encode()).hexdigest()

def create_access_token(user_id: str, role: str, session_id: str):
    # Simple Secure Token for Demo - Production માં JWT વાપરો
    import base64, json
    payload = {"user_id": user_id, "role": role, "session_id": session_id,
               "exp": (datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_MINUTES)).isoformat()}
    token = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()
    return token, payload["exp"]

def decode_token(token: str):
    import base64, json
    try:
        return json.loads(base64.urlsafe_b64decode(token).decode())
    except: return None
