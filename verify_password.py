def verify_password( password: str) -> bool:
        """Mock validate password functionality

        Args:
            password (str): Existing password of the user

        Returns: 
            bool: Whether the old password is valid
        """
        if "valid" in password:
            return True
        return False