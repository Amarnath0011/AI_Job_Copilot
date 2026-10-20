from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.auth import SignupRequest
from app.services.auth_service import (
    create_user,
    get_user_by_email,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/signup")
def signup(
    request: SignupRequest,
    db: Session = Depends(get_db),
):
    existing_user = get_user_by_email(
        db,
        request.email,
    )

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already registered",
        )

    user = create_user(
        db=db,
        name=request.name,
        email=request.email,
        password=request.password,
    )

    return {
        "message": "User created successfully",
        "user_id": user.id,
    }