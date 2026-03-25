from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.crud import crud
from app.core.config import settings
from app.db.database import get_db
from app.utils.utils import create_access_token, create_refresh_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

def _issue_tokens(entity_id: int, role: str, db: Session):
    token_payload = {"sub": entity_id, "user_type": role}
    access_token, _ = create_access_token(token_payload)
    refresh_token = create_refresh_token()
    expires_at = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    crud.create_session(db, refresh_token, role, entity_id, expires_at)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token,
    }

@router.post("/signup", response_model=schemas.AuthResponse, status_code=201)
def signup(payload: schemas.AuthSignup, db: Session = Depends(get_db)):
    from datetime import datetime, timedelta

    from fastapi import APIRouter, Depends, HTTPException
    from sqlalchemy.orm import Session

    from app import schemas
    from app.crud import crud
    from app.core.config import settings
    from app.db.database import get_db
    from app.utils.utils import create_access_token, create_refresh_token

    router = APIRouter(prefix="/auth", tags=["Authentication"])


    def _issue_tokens(entity_id: int, role: str, db: Session):
        token_payload = {"sub": entity_id, "user_type": role}
        access_token, _ = create_access_token(token_payload)
        refresh_token = create_refresh_token()
        expires_at = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

        crud.create_session(db, refresh_token, role, entity_id, expires_at)

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "refresh_token": refresh_token,
        }


    @router.post("/signup", response_model=schemas.AuthResponse, status_code=201)
    def signup(payload: schemas.AuthSignup, db: Session = Depends(get_db)):
        role = payload.role.lower()
        if role not in {"user", "company"}:
            raise HTTPException(status_code=400, detail="Invalid role")

        if role == "user":
            if crud.get_user_by_email(db, payload.email):
                raise HTTPException(status_code=400, detail="Email already registered")
            if crud.get_user_by_username(db, payload.username):
                raise HTTPException(status_code=400, detail="Username already taken")
            profile = crud.create_user(db, payload.username, payload.email, payload.password)
        else:
            if not payload.company_name:
                raise HTTPException(status_code=400, detail="company_name is required for company role")
            if crud.get_company_by_email(db, payload.email):
                raise HTTPException(status_code=400, detail="Email already registered")
            if crud.get_company_by_username(db, payload.username):
                raise HTTPException(status_code=400, detail="Username already taken")
            profile = crud.create_company(
                db,
                company_name=payload.company_name,
                username=payload.username,
                email=payload.email,
                password=payload.password,
            )

        token_data = _issue_tokens(profile.id, role, db)
        token = schemas.Token(**token_data)
        return schemas.AuthResponse(role=role, profile=profile, token=token)


    @router.post("/login", response_model=schemas.AuthResponse)
    def login(payload: schemas.AuthLogin, db: Session = Depends(get_db)):
        role = payload.role.lower()
        if role not in {"user", "company"}:
            raise HTTPException(status_code=400, detail="Invalid role")

        account = crud.authenticate_user(db, payload.email, payload.password, user_type=role)
        if not account:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token_data = _issue_tokens(account.id, role, db)
        token = schemas.Token(**token_data)
        return schemas.AuthResponse(role=role, profile=account, token=token)
