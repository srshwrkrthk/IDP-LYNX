from fastapi import APIRouter, HTTPException, status

from app.schemas.auth import RegisterRequest
from app.services.auth_service import register_user

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
            "message": "Registration successful. Check your email for verification.",
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