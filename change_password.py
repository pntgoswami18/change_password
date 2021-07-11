from difflib import SequenceMatcher
import string
from flask import abort
from verify_password import verify_password


class Password:
    def __init__(self):
        self.MIN_PASSWORD_LENGTH = 18

    def validate_repeat_characters_count(self, password: str, threshold: int) -> bool:
        """Counts repeat characters and checks if the count is less than threshold

        Args:
            password (str): Password string to validate
            threshold (int): Max value of repeat character count allowed

        Returns:
            bool: Whether the repeat character count is under threshold
        """
        character_count = {}
        for char in password:
            if char in character_count:
                if character_count[char] >= threshold:
                    return False
                else:
                    character_count[char] += 1
            else:
                character_count[char] = 1
        return True

    def validate_password_policy(self, password: str) -> bool:
        """Validate the password against password policy

        Args:
            password (str): Password to validate against password policy

        Returns:
            bool: Whether the password fulfills the password policy
        """
        # At least 18 alphanumeric characters and list of special chars !@#$&*
        if len(password) < self.MIN_PASSWORD_LENGTH:
            return False

        # At least 1 Upper case, 1 lower case ,least 1 numeric, 1 special character
        special_chars = set(string.punctuation)
        if (
            not any(char.isupper() for char in password)
            or not any(char.islower() for char in password)
            or not any(char.isnumeric() for char in password)
            or all(char not in special_chars for char in password)
        ):
            return False

        # No duplicate repeat characters more than 4
        if not self.validate_repeat_characters_count(password, 4):
            return False

        # No more than 4 special characters
        # 50 % of password should not be a number
        special_char_count = 0
        numeral_char_count = 0
        for char in password:
            if (special_char_count >= 4) or (numeral_char_count >= len(password)//2):
                return False
            if char in string.punctuation:
                special_char_count += 1
            elif char.isnumeric():
                numeral_char_count += 1
        return True

    def is_similar(self, old_password: str, new_password: str, threshold: float = 0.8) -> bool:
        """Check if the oldPassword and newPassword are similar considering the threshold value

        Args:
            oldPassword (str): Old password
            newPassword (str): New password
            threshold(float): Threshold of maximum allowed similarity [0.0 - 1.0]

        Returns:
            bool: whether the two passwords are similar w.r.t. threshold
        """
        return SequenceMatcher(None, old_password, new_password).ratio() >= threshold

    def ChangePassword(self, oldPassword: str, newPassword: str) -> bool:
        """Change the old password with the new password provided

        Args:
            oldPassword (str): The old password provided
            newPassword (str): The new password provided

        Returns:
            bool: whether the password change was successful
        """

        if not verify_password(oldPassword):
            return False

        # similar to old password < 80% match
        if self.is_similar(oldPassword, newPassword):
            return False

        # check new password for password policy
        return bool(self.validate_password_policy(newPassword))


def update_password(passwords) -> bool:
    old_password = passwords.get('old_password')
    new_password = passwords.get('new_password')
    password = Password()
    ret_value = password.ChangePassword(old_password, new_password)
    if ret_value == True:
        return ret_value
    else:
        abort(401, 'Change password failed ')
