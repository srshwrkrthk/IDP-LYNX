from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_current_user
from app.schemas.auth import LoginRequest, RegisterRequest
from app.services.auth_service import login_user, register_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(data: RegisterRequest):
    try:
        response = register_user(data.email, data.password)

        if response.user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Registration failed",
            )

        return {
            "message": "Registration successful",
            "user_id": str(response.user.id),
            "email": response.user.email,
        }

    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error


@router.post("/login")
def login(data: LoginRequest):
    try:
        response = login_user(data.email, data.password)

        if response.user is None or response.session is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        return {
            "message": "Login successful",
            "user": {
                "id": str(response.user.id),
                "email": response.user.email,
            },
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token,
            "token_type": "bearer",
            "expires_in": response.session.expires_in,
        }

    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        ) from error


@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "role": current_user.role,
    }