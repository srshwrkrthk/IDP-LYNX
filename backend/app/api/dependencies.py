from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.database import get_supabase

bearer = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(bearer),
):
    try:
        response = get_supabase().auth.get_user(credentials.credentials)

        if response.user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

        return response.user

    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        ) from error