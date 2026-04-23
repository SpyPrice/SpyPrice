from datetime import datetime, timedelta, timezone
from jose import jwt


SECRET_KEY = "хранить в env"
ALGORITHM = "HS256"


def create_access_token(data: dict, expires_minutes: int = 180) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
