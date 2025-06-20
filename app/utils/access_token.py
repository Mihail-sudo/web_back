from datetime import timedelta
from datetime import datetime as dt
from jose import jwt, JWTError
from fastapi import HTTPException


SECRET_KEY="1f14v2g45bg42fv24t"
ALGORITHM="HS256"

def create_access_token(username: str, id: int, expires_delta: timedelta):
    encode = {"sub": username, "id": id}
    expires = dt.utcnow() + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        user_id = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(status_code=401, detail="could not validate user")
        return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(status_code=401, detail="could not validate user")
    