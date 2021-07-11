def verify_password(password: str) -> bool:
    """Mock validate password functionality

    Args:
        password (str): Existing password of the user

    Returns: 
        bool: Whether the old password has the substring 'valid' in it
    """
    return "valid" in password
