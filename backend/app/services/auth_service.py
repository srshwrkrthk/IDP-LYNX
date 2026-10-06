from app.database import get_supabase


def register_user(email: str, password: str):
    return get_supabase().auth.sign_up(
        {
            "email": email,
            "password": password,
        }
    )


def login_user(email: str, password: str):
    return get_supabase().auth.sign_in_with_password(
        {
            "email": email,
            "password": password,
        }
    )