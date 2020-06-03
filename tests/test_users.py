import json
import time
import unittest

from unittest import skipIf
from unittest.mock import Mock, patch
from oktaadminapi import create_app


class TestVerifier(unittest.TestCase):
    def setUp(self):
        self.user_id = "00umsmn2zeHhlu3sY0h7"
        self.not_a_real_user_id = "notarealuserid"
        self.app = create_app().test_client()

    def tearDown(self):
        pass

    def test_get_user_no_token_returns_unauthorized(self):
        response = self.app.get("/api/v1/users/{0}".format(self.user_id))
        print(response.data)
        self.assertEqual(401, response.status_code)

    def test_get_user_with_invalid_id_returns_404(self):
        response = self.app.get("/api/v1/users/{0}".format(self.not_a_real_user_id))
        self.assertEqual(404, response.status_code)
