from typing import Optional
import bcrypt
from fastapi import HTTPException, Depends
from jose import jwt, JWTError
from repositories import UserRepository
from datetime import datetime, timedelta
from core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, OAUTH2_SCHEME


class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()

    def authenticate_user(self, email: str, password: str) -> Optional[dict]:
        user = self.user_repo.get_by_email(email)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        stored_password = user["password"].encode('utf-8')
        if not bcrypt.checkpw(password.encode('utf-8'), stored_password):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        return user

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def verify_token(token: str = Depends(OAUTH2_SCHEME)):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: str = payload.get("sub")
            if user_id is None:
                raise HTTPException(status_code=401, detail="Invalid token")
            return user_id
        except JWTError:
            raise HTTPException(status_code=401, detail="Could not validate credentials")