from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.db.database import get_db
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
)
from app.services.auth_service import (
    register_user,
    login_user,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
):
    user = register_user(
        db,
        request.full_name,
        request.email,
        request.password,
    )

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )

    return {
        "message": "User registered successfully",
        "user_id": str(user.id),
    }


@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    token = login_user(
        db,
        form_data.username,
        form_data.password,
    )

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    return {
        "access_token": token,
        "token_type": "bearer",
    }