from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt, ExpiredSignatureError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.database import get_db
from app.crud.crud import get_user_by_id, get_company_by_id

bearer_scheme = HTTPBearer(auto_error=False)

def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    from fastapi import Depends, HTTPException
    from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
    from jose import JWTError, jwt
    from jose.exceptions import ExpiredSignatureError
    from sqlalchemy.orm import Session

    from app.core.config import settings
    from app.db.database import get_db
    from app.crud.crud import get_user_by_id, get_company_by_id

    bearer_scheme = HTTPBearer(auto_error=False)


    def decode_token(token: str) -> dict:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            return payload
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")


    def get_current_user_id(
        creds: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    ):
        if not creds:
            raise HTTPException(status_code=401, detail="Authentication credentials were not provided")

        token_data = decode_token(creds.credentials)
        if token_data.get("user_type") != "user":
            raise HTTPException(status_code=403, detail="User credentials required")

        return token_data["sub"]


    def get_current_company_id(
        creds: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    ):
        if not creds:
            raise HTTPException(status_code=401, detail="Authentication credentials were not provided")

        token_data = decode_token(creds.credentials)
        if token_data.get("user_type") != "company":
            raise HTTPException(status_code=403, detail="Company credentials required")

        return token_data["sub"]


    def get_current_user(
        creds: HTTPAuthorizationCredentials = Depends(bearer_scheme),
        db: Session = Depends(get_db)
    ):
        if not creds:
            raise HTTPException(status_code=401, detail="Authentication credentials were not provided")

        token_data = decode_token(creds.credentials)
        if token_data.get("user_type") != "user":
            raise HTTPException(status_code=403, detail="User credentials required")

        user = get_user_by_id(db, token_data["sub"])
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user


    def get_current_company(
        creds: HTTPAuthorizationCredentials = Depends(bearer_scheme),
        db: Session = Depends(get_db)
    ):
        if not creds:
            raise HTTPException(status_code=401, detail="Authentication credentials were not provided")

        token_data = decode_token(creds.credentials)
        if token_data.get("user_type") != "company":
            raise HTTPException(status_code=403, detail="Company credentials required")

        company = get_company_by_id(db, token_data["sub"])
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")

        return company
