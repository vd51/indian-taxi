from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from backend.core.security import decode_token
from backend.core.database import get_db
from pydantic import BaseModel
security = HTTPBearer(auto_error=False)
class AuthenticatedUser(BaseModel):
    id: str; phone: str; role: str; full_name: str
def get_current_user(creds: HTTPAuthorizationCredentials = Depends(security), db = Depends(get_db)):
    if not creds: raise HTTPException(status_code=401, detail="Token missing - Login કરો")
    data = decode_token(creds.credentials)
    if not data: raise HTTPException(status_code=401, detail="Invalid token")
    row = db.execute("SELECT * FROM users WHERE id=?", (data["user_id"],)).fetchone()
    if not row: raise HTTPException(status_code=401, detail="User not found")
    return AuthenticatedUser(id=row["id"], phone=row["phone"], role=row["role"], full_name=row["full_name"])
