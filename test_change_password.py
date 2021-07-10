import unittest
from change_password import Password
from unittest.mock import patch


class TestChangePassword(unittest.TestCase):
    @patch('change_password.verify_password')
    def test_ChangePassword_success(self, mock_verify_password):
        mock_verify_password.return_value = True

        password = Password()
        ret_value = password.ChangePassword(
            'myWesdrtsfdsrgrf', 'myNewPassword@123456')
        self.assertTrue(ret_value, 'Change password failed')

    @patch('change_password.verify_password')
    def test_ChangePassword_failure_similar_password(self, mock_verify_password):
        mock_verify_password.return_value = False
        password = Password()
        ret_value = password.ChangePassword(
            'myOldPassword', 'myNewPassword@$12345')
        self.assertFalse(ret_value, 'Change password similarity check failed')

    @patch('change_password.verify_password')
    def test_ChangePassword_failure_min_length(self, mock_verify_password):
        mock_verify_password.return_value = False
        password = Password()
        ret_value = password.ChangePassword(
            'myOldPassword', 'myNewPassword@$12')
        self.assertFalse(
            ret_value, 'Change password minimum length check failed')

    @patch('change_password.verify_password')
    def test_ChangePassword_failure_uppercase(self, mock_verify_password):
        mock_verify_password.return_value = False
        password = Password()
        ret_value = password.ChangePassword(
            'myOldPassword', 'mynewpassword@123456')
        self.assertFalse(
            ret_value, 'Change password uppercase character check failed')

    @patch('change_password.verify_password')
    def test_ChangePassword_failure_lowercase(self, mock_verify_password):
        mock_verify_password.return_value = False
        password = Password()
        ret_value = password.ChangePassword(
            'myOldPassword', 'MYNEWPASSWORD@123456')
        self.assertFalse(
            ret_value, 'Change password lowercase character check failed')

    @patch('change_password.verify_password')
    def test_ChangePassword_failure_numeric(self, mock_verify_password):
        mock_verify_password.return_value = False
        password = Password()
        ret_value = password.ChangePassword(
            'myOldPassword', 'mynewpassword@UPPERLET')
        self.assertFalse(
            ret_value, 'Change password numeric character check failed')

    @patch('change_password.verify_password')
    def test_ChangePassword_failure_specialchar(self, mock_verify_password):
        mock_verify_password.return_value = False
        password = Password()
        ret_value = password.ChangePassword(
            'myOldPassword', 'mynewpasswordA123456')
        self.assertFalse(
            ret_value, 'Change password special character check failed')

    @patch('change_password.verify_password')
    def test_ChangePassword_failure_duplicate_char(self, mock_verify_password):
        mock_verify_password.return_value = False
        password = Password()
        ret_value = password.ChangePassword(
            'myOldPassword', 'mynewpassssword@123456')
        self.assertFalse(
            ret_value, 'Change password duplicate characters check failed')

    @patch('change_password.verify_password')
    def test_ChangePassword_failure_max_specialchar(self, mock_verify_password):
        mock_verify_password.return_value = False
        password = Password()
        ret_value = password.ChangePassword(
            'myOldPassword', 'mynewpa$sw*rd@1#345&')
        self.assertFalse(
            ret_value, 'Change password maximum special character check failed')

    @patch('change_password.verify_password')
    def test_ChangePassword_failure_max_numeric(self, mock_verify_password):
        mock_verify_password.return_value = False
        password = Password()
        ret_value = password.ChangePassword(
            'myOldPassword', 'myN3wPa55w0rd@123456!')
        self.assertFalse(
            ret_value, 'Change password maximum numeric character check failed')

    @patch('change_password.verify_password')
    def test_ChangePassword_no_new_password(self, mock_verify_password):
        mock_verify_password.side_effect = TypeError
        password = Password()
        with self.assertRaises(TypeError):
            password.ChangePassword('myOldPassword')


if __name__ == '__main__':
    unittest.main()
