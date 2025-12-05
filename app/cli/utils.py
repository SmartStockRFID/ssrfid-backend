def validate_username(username: str) -> bool:
    return len(username) >= 3


def validate_email(email: str) -> bool:
    return "@" in email and "." in email
