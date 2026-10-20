from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.security import create_access_token
from app.db.database import get_db
from app.db.models import User
from app.models.auth import AuthResponse, LoginRequest, SignupRequest, UserResponse
from app.services.auth_service import authenticate_user, create_user, get_user_by_email

router = APIRouter(prefix="/auth", tags=["Authentication"])


def _auth_response(user: User) -> AuthResponse:
    return AuthResponse(
        access_token=create_access_token(user.id),
        user=UserResponse(id=user.id, full_name=user.name, email=user.email),
    )


@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    email = str(payload.email).lower().strip()
    if get_user_by_email(db, email):
        raise HTTPException(status_code=409, detail="An account with this email already exists.")
    try:
        user = create_user(db, payload.full_name, email, payload.password)
        return _auth_response(user)
    except ValueError as exc:
        db.rollback()
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="An account with this email already exists.") from exc


@router.post("/login", response_model=AuthResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, str(payload.email), payload.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return _auth_response(user)


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse(id=current_user.id, full_name=current_user.name, email=current_user.email)
