from app.database import get_supabase


def register_user(email: str, password: str):
    supabase = get_supabase()

    return supabase.auth.sign_up(
        {
            "email": email,
            "password": password,
        }
    )