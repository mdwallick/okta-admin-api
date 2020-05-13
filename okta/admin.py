import json
import logging
import os

from okta.util import OktaUtil
from okta.rest import RestUtil

class OktaAdmin:

    #logger = logging.getLogger(__name__)

    okta_config = {
        "okta_org_name": os.getenv("OKTA_ORG_NAME"),
        "okta_api_token": os.getenv("OKTA_API_TOKEN"),
        "client_id": os.getenv("CLIENT_ID")
    }

    #def __init__(self):
        #self.logger.debug("OktaAdmin init()")
        #self.logger.info("okta_config: {0}".format(self.okta_config))

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

    def get_groups_by_name(self, name):
        #self.logger.debug("OktaAdmin.get_groups_by_name(name)")
        okta_headers = OktaUtil.get_protected_okta_headers(self.okta_config)
        url = "{base_url}/api/v1/groups?q={name}".format(
            base_url=self.okta_config["okta_org_name"],
            name=name
        )
        return RestUtil.execute_get(url, okta_headers)

    def assign_user_to_group(self, group_id, user_id):
        #self.logger.debug("OktaAdmin.assign_user_to_group(group_id, user_id)")
        okta_headers = OktaUtil.get_protected_okta_headers(self.okta_config)
        url = "{base_url}/api/v1/groups/{group_id}/users/{user_id}".format(
            base_url=self.okta_config["okta_org_name"],
            group_id=group_id,
            user_id=user_id
        )
        body = {}
        return RestUtil.execute_put(url, body, okta_headers)

    def get_applications_by_user_id(self, user_id):
        #self.logger.debug("OktaAdmin.get_applications_by_user_id(user_id)")
        okta_headers = OktaUtil.get_protected_okta_headers(self.okta_config)
        url = "{base_url}/api/v1/apps/?filter=user.id+eq+\"{user_id}\"".format(
            base_url=self.okta_config["okta_org_name"],
            user_id=user_id
        )
        return RestUtil.execute_get(url, okta_headers)

    def get_user_application_by_current_client_id(self, user_id):
        #self.logger.debug("OktaAdmin.get_user_application_by_current_client_id()")
        okta_headers = OktaUtil.get_protected_okta_headers(self.okta_config)
        url = "{base_url}/api/v1/apps/{app_id}/users/{user_id}".format(
            base_url=self.okta_config["okta_org_name"],
            app_id=self.okta_config["client_id"],
            user_id=user_id
        )
        return RestUtil.execute_get(url, okta_headers)

    def update_application_user_profile(self, user_id, app_user_profile):
        #self.logger.debug("OktaAdmin.update_application_user_profile()")
        #self.logger.debug("App user profile: {0}".format(json.dumps(app_user_profile)))
        okta_headers = OktaUtil.get_protected_okta_headers(self.okta_config)
        url = "{base_url}/api/v1/apps/{app_id}/users/{user_id}".format(
            base_url=self.okta_config["okta_org_name"],
            app_id=self.okta_config["client_id"],
            user_id=user_id
        )
        body = { "profile": app_user_profile["profile"] }
        return RestUtil.execute_post(url, body, okta_headers)

    def close_session(self, session_id):
        #self.logger.debug("OktaAdmin.close_session(session_id)")
        okta_headers = OktaUtil.get_protected_okta_headers(self.okta_config)
        url = "{base_url}/api/v1/sessions/{session_id}".format(
            base_url=self.okta_config["okta_org_name"],
            session_id=session_id
        )
        body = {}
        return RestUtil.execute_delete(url, body, okta_headers)