import json
import logging
import os

from okta.util import OktaUtil
from okta.rest import RestUtil

class OktaUsers:

    logger = logging.getLogger(__name__)

    okta_config = {
        "okta_org_name": os.getenv("OKTA_ORG_NAME"),
        "okta_api_token": os.getenv("OKTA_API_TOKEN")
    }

    def __init__(self):
        self.logger.debug("OktaUsers init()")
        self.logger.debug("okta_config: {0}".format(self.okta_config))

    def get_user(self, user_id):
        #self.logger.debug("OktaAdmin.get_user(user_id)")
        okta_headers = OktaUtil.get_protected_okta_headers(self.okta_config)
        url = "{base_url}/api/v1/users/{user_id}".format(
            base_url=self.okta_config["okta_org_name"],
            user_id=user_id)
        return RestUtil.execute_get(url, okta_headers)

    def get_user_groups(self, user_id):
        #self.logger.debug("OktaAdmin.get_user_groups(user_id)")
        okta_headers = OktaUtil.get_protected_okta_headers(self.okta_config)
        url = "{base_url}/api/v1/users/{user_id}/groups".format(
            base_url=self.okta_config["okta_org_name"],
            user_id=user_id)
        return RestUtil.execute_get(url, okta_headers)

    def create_user(self, user, activate_user=False):
        #self.logger.debug("OktaAdmin.create_user(user)")
        okta_headers = OktaUtil.get_protected_okta_headers(self.okta_config)
        url = "{base_url}/api/v1/users?activate={activate_user}".format(
            base_url=self.okta_config["okta_org_name"],
            activate_user=activate_user)
        return RestUtil.execute_post(url, user, okta_headers)

    def update_user(self, user_id, user):
        #self.logger.debug("OktaAdmin.update_user()")
        #self.logger.debug("User profile: {0}".format(json.dumps(user)))
        okta_headers = OktaUtil.get_protected_okta_headers(self.okta_config)
        url = "{base_url}/api/v1/users/{user_id}".format(
            base_url=self.okta_config["okta_org_name"],
            user_id=user_id)
        return RestUtil.execute_post(url, user, okta_headers)

    def activate_user(self, user_id, send_email=True):
        #self.logger.debug("OktaAdmin.activate_user(user_id)")
        okta_headers = OktaUtil.get_protected_okta_headers(self.okta_config)
        url = "{base_url}/api/v1/users/{user_id}/lifecycle/activate/?sendEmail={send_email}".format(
            base_url=self.okta_config["okta_org_name"],
            user_id=user_id,
            send_email=str(send_email).lower()
        )
        body = {}
        return RestUtil.execute_post(url, body, okta_headers)
