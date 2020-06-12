import json
import time
import unittest

from flask_api import status
from unittest import skipIf
from unittest.mock import Mock, patch
from oktaadminapi import create_app


class TestFactors(unittest.TestCase):
    def setUp(self):
        self.factor_id = "ufsrxakzuoLFbpzkI0h7"
        self.user_id = "00umsmn2zeHhlu3sY0h7"
        self.not_a_real_factor_id = "notarealfactorid"
        # use prodconfig to suppress all the debug
        # messaging while running tests
        self.app = create_app(config_class="config.ProdConfig")
        self.client = self.app.test_client()

    def tearDown(self):
        pass

    def test_get_factor_no_token_returns_unauthorized(self):
        uri = "/api/v1/users/{0}/factors/{1}".format(self.user_id, self.factor_id)
        response = self.client.get(uri)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_get_enrolled_factors_no_token_returns_unauthorized(self):
        uri = "/api/v1/users/{0}/factors".format(self.user_id)
        response = self.client.get(uri)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_get_available_factors_no_token_returns_unauthorized(self):
        uri = "/api/v1/users/{0}/factors/catalog".format(self.user_id)
        response = self.client.get(uri)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_get_available_questions_no_token_returns_unauthorized(self):
        uri = "/api/v1/users/{0}/factors/questions".format(self.user_id)
        response = self.client.get(uri)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_enroll_factor_no_token_returns_unauthorized(self):
        uri = "/api/v1/users/{0}/factors/question".format(self.user_id)
        response = self.client.post(uri)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_poll_push_activation_no_token_returns_unauthorized(self):
        uri = "/api/v1/users/{0}/factors/{1}/activate/push".format(self.user_id, self.factor_id)
        response = self.client.post(uri)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_activate_otp_no_token_returns_unauthorized(self):
        uri = "/api/v1/users/{0}/factors/{1}/activate/totp".format(self.user_id, self.factor_id)
        response = self.client.post(uri)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_verify_factor_no_token_returns_unauthorized(self):
        uri = "/api/v1/users/{0}/factors/{1}/verify".format(self.user_id, self.factor_id)
        response = self.client.post(uri)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_poll_push_verification_no_token_returns_unauthorized(self):
        uri = "/api/v1/users/{0}/factors/{1}/verify/push".format(self.user_id, self.factor_id)
        response = self.client.post(uri)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    # def test_get_factor_with_invalid_id_returns_404(self):
    #     uri = "/api/v1/users/{0}/factors/{1}".format(self.user_id, self.not_a_real_factor_id)
    #     response = self.client.get(uri)
    #     self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
