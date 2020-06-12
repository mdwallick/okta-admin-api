import json
import time
import unittest

from flask_api import status
from unittest import skipIf
from unittest.mock import Mock, patch
from oktaadminapi import create_app


class TestGroups(unittest.TestCase):
    def setUp(self):
        self.group_id = "00grsuobu6NnfNXo30h7"
        self.user_id = "00umsmn2zeHhlu3sY0h7"
        self.not_a_real_group_id = "notarealgroupid"
        # use prodconfig to suppress all the debug
        # messaging while running tests
        self.app = create_app(config_class="config.ProdConfig")
        self.client = self.app.test_client()

    def tearDown(self):
        pass

    def test_get_group_no_token_returns_unauthorized(self):
        uri = "/api/v1/groups/{0}".format(self.group_id)
        response = self.client.get(uri)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_get_groups_no_token_returns_unauthorized(self):
        uri = "/api/v1/groups"
        response = self.client.get(uri)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_create_group_no_token_returns_unauthorized(self):
        uri = "/api/v1/groups"
        response = self.client.post(uri)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_update_group_no_token_returns_unauthorized(self):
        uri = "/api/v1/groups/{0}".format(self.user_id)
        response = self.client.put(uri)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_delete_group_no_token_returns_unauthorized(self):
        uri = "/api/v1/groups/{0}".format(self.user_id)
        response = self.client.delete(uri)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_get_group_users_no_token_returns_unauthorized(self):
        uri = "/api/v1/groups/{0}/users".format(self.user_id)
        response = self.client.get(uri)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_add_user_to_group_no_token_returns_unauthorized(self):
        uri = "/api/v1/groups/{0}/users/{1}".format(self.group_id, self.user_id)
        response = self.client.put(uri)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_remove_user_from_group_no_token_returns_unauthorized(self):
        uri = "/api/v1/groups/{0}/users/{1}".format(self.group_id, self.user_id)
        response = self.client.delete(uri)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    # def test_get_group_with_invalid_id_returns_404(self):
    #     uri = "/api/v1/groups/{0}".format(self.not_a_real_group_id)
    #     response = self.client.get(uri)
    #     self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
