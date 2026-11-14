import json, logging, secrets, uuid, hmac
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from backend.core.config import settings
from backend.core.database import get_db
from backend.core.security import hash_password, verify_password, hash_otp, create_access_token
from backend.schemas.auth import RegisterRequest, OTPVerifyRequest, LoginRequest
from backend.middleware.auth import get_current_user, AuthenticatedUser

router = APIRouter()
logger = logging.getLogger("indian_taxi.auth")
def utc_now(): return datetime.now(timezone.utc)
def iso_time(v): return v.isoformat()

def create_session(db, user_id, role):
    now = utc_now(); session_id = str(uuid.uuid4())
    exp = now + timedelta(days=settings.SESSION_DAYS)
    db.execute("INSERT INTO auth_sessions (id,user_id,expires_at,created_at,last_seen_at) VALUES (?,?,?,?,?)",
               (session_id, user_id, iso_time(exp), iso_time(now), iso_time(now)))
    db.commit()
    token, _ = create_access_token(user_id, role, session_id)
    return {"access_token": token, "token_type": "bearer", "expires_in": settings.ACCESS_TOKEN_MINUTES*60, "session_expires_at": iso_time(exp)}

@router.post("/register/request", status_code=202)
def request_registration_otp(data: RegisterRequest, db=Depends(get_db)):
    phone = data.phone.strip().replace(" ", "").replace("+91","")
    if len(phone)!=10 or not phone.isdigit() or phone[0] not in "6789":
        raise HTTPException(400, "માન્ય 10 અંકનો ભારતીય મોબાઇલ નંબર આપો")
    if db.execute("SELECT id FROM users WHERE phone=?", (phone,)).fetchone():
        raise HTTPException(409, "This mobile number is already registered.")
    now = utc_now(); cutoff = iso_time(now - timedelta(minutes=15))
    recent = db.execute("SELECT COUNT(*) as t FROM otp_challenges WHERE phone=? AND created_at>=?", (phone, cutoff)).fetchone()["t"]
    if recent >= 5: raise HTTPException(429, "Too many OTP requests. Try again later.")
    last = db.execute("SELECT created_at FROM otp_challenges WHERE phone=? ORDER BY created_at DESC LIMIT 1", (phone,)).fetchone()
    if last and now - datetime.fromisoformat(last["created_at"]) < timedelta(seconds=60):
        raise HTTPException(429, "Please wait 60 seconds before requesting another OTP.")
    cid = str(uuid.uuid4()); otp = f"{secrets.randbelow(1_000_000):06d}"
    exp = now + timedelta(minutes=settings.OTP_MINUTES)
    payload = {"full_name": data.full_name, "email": data.email, "password_hash": hash_password(data.password)}
    db.execute("INSERT INTO otp_challenges (id,phone,purpose,otp_hash,payload_json,attempts,expires_at,consumed_at,created_at) VALUES (?,?,?,?,?,0,?,NULL,?)",
               (cid, phone, 'registration', hash_otp(cid, otp), json.dumps(payload), iso_time(exp), iso_time(now)))
    db.commit()
    resp = {"success": True, "message": "OTP challenge created.", "challenge_id": cid, "expires_in": settings.OTP_MINUTES*60, "delivery": "development_only"}
    if settings.OTP_EXPOSE_IN_DEVELOPMENT:
        resp["dev_otp"] = otp
        print(f"🔐 DEV OTP for {phone}: {otp}")
    return resp

@router.post("/register/verify")
def verify_registration_otp(data: OTPVerifyRequest, db=Depends(get_db)):
    phone = data.phone.strip().replace(" ", "").replace("+91","")
    now = utc_now()
    ch = db.execute("SELECT * FROM otp_challenges WHERE id=? AND phone=? AND purpose='registration' AND consumed_at IS NULL", (data.challenge_id, phone)).fetchone()
    if not ch: raise HTTPException(400, "Invalid or expired OTP challenge.")
    if datetime.fromisoformat(ch["expires_at"]) <= now: raise HTTPException(400, "OTP has expired. Request a new OTP.")
    if ch["attempts"] >= settings.OTP_MAX_ATTEMPTS: raise HTTPException(429, "Maximum OTP attempts exceeded.")
    db.execute("UPDATE otp_challenges SET attempts=attempts+1 WHERE id=?", (data.challenge_id,))
    if not hmac.compare_digest(hash_otp(data.challenge_id, data.otp), ch["otp_hash"]):
        db.commit(); raise HTTPException(400, "Incorrect OTP.")
    payload = json.loads(ch["payload_json"])
    uid = str(uuid.uuid4()); pid = str(uuid.uuid4())
    db.execute("INSERT INTO users (id,full_name,phone,email,password_hash,role,is_verified,created_at) VALUES (?,?,?,?,?,'passenger',1,?)",
               (uid, payload["full_name"], phone, payload["email"], payload["password_hash"], iso_time(now)))
    db.execute("INSERT INTO passengers (id,user_id,wallet_balance) VALUES (?,?,0)", (pid, uid))
    db.execute("UPDATE otp_challenges SET consumed_at=? WHERE id=?", (iso_time(now), data.challenge_id))
    db.commit()
    sess = create_session(db, uid, 'passenger')
    return {"success": True, "message": "Account created successfully!", "user": {"id": uid, "full_name": payload["full_name"], "phone": phone, "role": "passenger"}, **sess}

@router.post("/login")
def login(data: LoginRequest, db=Depends(get_db)):
    phone = data.phone.strip().replace(" ", "").replace("+91","")
    user = db.execute("SELECT * FROM users WHERE phone=?", (phone,)).fetchone()
    if not user or not verify_password(data.password, user["password_hash"]):
        raise HTTPException(401, "Invalid mobile number or password.")
    sess = create_session(db, user["id"], user["role"])
    return {"success": True, "message": "Login successful", "user": {"id": user["id"], "full_name": user["full_name"], "phone": user["phone"], "role": user["role"]}, **sess}

@router.post("/logout")
def logout(user: AuthenticatedUser = Depends(get_current_user), db=Depends(get_db)):
    db.execute("DELETE FROM auth_sessions WHERE user_id=?", (user.id,)); db.commit()
    return {"success": True, "message": "Logged out successfully"}

@router.get("/me")
def me(user: AuthenticatedUser = Depends(get_current_user)):
    return {"success": True, "user": user.dict()}
