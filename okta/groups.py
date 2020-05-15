import json
import logging
import os

from okta.util import OktaUtil
from okta.rest import RestUtil

class OktaGroups:

    logger = logging.getLogger(__name__)

    okta_config = {
        "okta_org_name": os.getenv("OKTA_ORG_NAME"),
        "okta_api_token": os.getenv("OKTA_API_TOKEN")
    }

    def __init__(self):
        self.logger.debug("OktaAdmin init()")
        self.logger.debug("okta_config: {0}".format(self.okta_config))

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

