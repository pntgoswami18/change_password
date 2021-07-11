import unittest
from change_password import Password, update_password
from unittest.mock import patch
from webserver import app
import json

_PASSWORD_API_ROUTE = '/api/password'


class TestChangePassword(unittest.TestCase):
    webapp = app.app
    webapp.config['TESTING'] = True
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/problem+json'
    }

    @patch('change_password.verify_password')
    def test_ChangePassword_success(self, mock_verify_password):
        mock_verify_password.return_value = True

        password = Password()
        ret_value = password.ChangePassword(
            'myWesdrtsfdsrgrf', 'myNewPassword@123456')
        self.assertTrue(ret_value, 'Change password failed')

    @patch('change_password.verify_password')
    def test_ChangePassword_failure_similar_password(self, mock_verify_password):
        mock_verify_password.return_value = True
        password = Password()
        ret_value = password.ChangePassword(
            'myNewPassword', 'myNewPassword@12345')
        self.assertFalse(ret_value, 'Change password similarity check failed')

    @patch('change_password.verify_password')
    def test_ChangePassword_failure_min_length(self, mock_verify_password):
        mock_verify_password.return_value = True
        password = Password()
        ret_value = password.ChangePassword(
            'myOldPassword', 'myNewPassword@$12')
        self.assertFalse(
            ret_value, 'Change password minimum length check failed')

    @patch('change_password.verify_password')
    def test_ChangePassword_failure_uppercase(self, mock_verify_password):
        mock_verify_password.return_value = True
        password = Password()
        ret_value = password.ChangePassword(
            'myOldPassword', 'mynwpassword@123456')
        self.assertFalse(
            ret_value, 'Change password uppercase character check failed')

    @patch('change_password.verify_password')
    def test_ChangePassword_failure_lowercase(self, mock_verify_password):
        mock_verify_password.return_value = True
        password = Password()
        ret_value = password.ChangePassword(
            'myOldPassword', 'MYNEPASSWORD@123456')
        self.assertFalse(
            ret_value, 'Change password lowercase character check failed')

    @patch('change_password.verify_password')
    def test_ChangePassword_failure_numeric(self, mock_verify_password):
        mock_verify_password.return_value = True
        password = Password()
        ret_value = password.ChangePassword(
            'myOldPassword', 'mynewpassword@UPPERLET')
        self.assertFalse(
            ret_value, 'Change password numeric character check failed')

    @patch('change_password.verify_password')
    def test_ChangePassword_failure_specialchar(self, mock_verify_password):
        mock_verify_password.return_value = True
        password = Password()
        ret_value = password.ChangePassword(
            'myOldPassword', 'mynewpasswordA123456')
        self.assertFalse(
            ret_value, 'Change password special character check failed')

    @patch('change_password.verify_password')
    def test_ChangePassword_failure_duplicate_char(self, mock_verify_password):
        mock_verify_password.return_value = True
        password = Password()
        ret_value = password.ChangePassword(
            'myOldPassword', 'mynewpassssword@123456')
        self.assertFalse(
            ret_value, 'Change password duplicate characters check failed')

    @patch('change_password.verify_password')
    def test_ChangePassword_failure_max_specialchar(self, mock_verify_password):
        mock_verify_password.return_value = True
        password = Password()
        ret_value = password.ChangePassword(
            'myOldPassword', 'mynewpa$sw*rd@1#345&')
        self.assertFalse(
            ret_value, 'Change password maximum special character check failed')

    @patch('change_password.verify_password')
    def test_ChangePassword_failure_max_numeric(self, mock_verify_password):
        mock_verify_password.return_value = True
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

    def test_changePassword_update_password(self):
        passwords = {
            'old_password': 'validOldPassword',
            'new_password': 'someNewPassword@123'
        }
        self.assertTrue(update_password(passwords),
                        'update_password for valid passwords object failed')

    def test_changePassword_update_password_abort(self):
        passwords = {
            'old_password': 'myOldPassword',
            'new_password': 'someNewPassword@123'
        }
        with self.assertRaises(Exception):
            update_password(passwords)

    def test_app_home_page(self):
        response = self.webapp.test_client().get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_app_change_password(self):
        data = {'old_password': 'myvalidWesdrtsfdsrgrf',
                'new_password': 'MyNewPassword@123456'}
        response = self.webapp.test_client().put(
            _PASSWORD_API_ROUTE, data=json.dumps(data), headers=self.headers)
        self.assertEqual(response.status_code, 200,
                         'Password change API did not change password')

    def test_app_change_password_failure(self):
        data = {'old_password': 'myWesdrtsfdsrgrf',
                'new_password': 'myNewPassworD@123456'}
        response = self.webapp.test_client().put(
            _PASSWORD_API_ROUTE, data=json.dumps(data), headers=self.headers)
        self.assertEqual(response.status_code, 401,
                         'Old Password verification failed in API')

        data['old_password'] = 'myvalidOldPassword'
        data['new_password'] = 'myNewPassword@$12'
        response = self.webapp.test_client().put(
            _PASSWORD_API_ROUTE, data=json.dumps(data), headers=self.headers)
        self.assertEqual(response.status_code, 401,
                         'Password minimum length verification failed in API')


if __name__ == '__main__':
    unittest.main()
