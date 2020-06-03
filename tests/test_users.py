import json
import time
import unittest

from flask_api import status
from unittest import skipIf
from unittest.mock import Mock, patch
from oktaadminapi import create_app


class TestVerifier(unittest.TestCase):
    def setUp(self):
        self.user_id = "00umsmn2zeHhlu3sY0h7"
        self.not_a_real_user_id = "notarealuserid"
        # use prodconfig to suppress all the debug
        # messaging while running tests
        self.app = create_app(config_class="config.ProdConfig")
        self.client = self.app.test_client()

    def tearDown(self):
        pass

    def test_get_user_no_token_returns_unauthorized(self):
        uri = "/api/v1/users/{0}".format(self.user_id)
        response = self.client.get(uri)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_get_users_no_token_returns_unauthorized(self):
        uri = "/api/v1/users"
        response = self.client.get(uri)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_create_user_no_token_returns_unauthorized(self):
        uri = "/api/v1/users"
        response = self.client.post(uri)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_update_user_no_token_returns_unauthorized(self):
        uri = "/api/v1/users/{0}".format(self.user_id)
        response = self.client.put(uri)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_delete_user_no_token_returns_unauthorized(self):
        uri = "/api/v1/users/{0}".format(self.user_id)
        response = self.client.delete(uri)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_get_user_applinks_no_token_returns_unauthorized(self):
        uri = "/api/v1/users/{0}/appLinks".format(self.user_id)
        response = self.client.get(uri)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_get_user_groups_no_token_returns_unauthorized(self):
        uri = "/api/v1/users/{0}/groups".format(self.user_id)
        response = self.client.get(uri)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_forgot_password_no_token_returns_unauthorized(self):
        uri = "/api/v1/users/{0}/credentials/forgot_password".format(self.user_id)
        response = self.client.post(uri)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_change_password_no_token_returns_unauthorized(self):
        uri = "/api/v1/users/{0}/credentials/change_password".format(self.user_id)
        response = self.client.post(uri)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_change_recovery_question_no_token_returns_unauthorized(self):
        uri = "/api/v1/users/{0}/credentials/change_recovery_question".format(self.user_id)
        response = self.client.post(uri)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_expire_password_no_token_returns_unauthorized(self):
        uri = "/api/v1/users/{0}/lifecycle/expire_password".format(self.user_id)
        response = self.client.post(uri)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_reset_password_no_token_returns_unauthorized(self):
        uri = "/api/v1/users/{0}/lifecycle/reset_password".format(self.user_id)
        response = self.client.post(uri)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_activate_user_no_token_returns_unauthorized(self):
        uri = "/api/v1/users/{0}/lifecycle/activate".format(self.user_id)
        response = self.client.post(uri)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_deactivate_user_no_token_returns_unauthorized(self):
        uri = "/api/v1/users/{0}/lifecycle/deactivate".format(self.user_id)
        response = self.client.post(uri)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_suspend_user_no_token_returns_unauthorized(self):
        uri = "/api/v1/users/{0}/lifecycle/suspend".format(self.user_id)
        response = self.client.post(uri)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_unsuspend_user_no_token_returns_unauthorized(self):
        uri = "/api/v1/users/{0}/lifecycle/unsuspend".format(self.user_id)
        response = self.client.post(uri)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_unlock_user_no_token_returns_unauthorized(self):
        uri = "/api/v1/users/{0}/lifecycle/unlock".format(self.user_id)
        response = self.client.post(uri)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_reset_factors_no_token_returns_unauthorized(self):
        uri = "/api/v1/users/{0}/lifecycle/reset_factors".format(self.user_id)
        response = self.client.post(uri)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    # def test_get_user_with_invalid_id_returns_404(self):
    #     uri = "/api/v1/users/{0}".format(self.not_a_real_user_id)
    #     response = self.client.get(uri)
    #     self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
