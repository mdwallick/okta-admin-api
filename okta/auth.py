import json
import logging
import os

from okta.util import OktaUtil
from okta.rest import RestUtil

class OktaAuth:

    #logger = logging.getLogger(__name__)

    okta_config = {
        "okta_org_name": os.getenv("OKTA_ORG_NAME"),
        "issuer": os.getenv("ISSUER"),
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET")
    }

    # def __init__(self):
    #     self.logger.debug("OktaAuth init()")
    #     self.logger.info("okta_config: {0}".format(self.okta_config))

    def authenticate(self, username, password, additional_options=None, headers=None):
        #self.logger.debug("OktaAuth.authenticate()")
        url = "{host}/api/v1/authn".format(host=self.okta_config["okta_org_name"])
        okta_headers = OktaUtil.get_default_okta_headers(headers)

        body = {
            "username": username,
            "password": password,
        }

        if additional_options:
            RestUtil.map_attribute("audience", additional_options, body)
            RestUtil.map_attribute("relayState", additional_options, body)
            RestUtil.map_attribute("options", additional_options, body)
            RestUtil.map_attribute("context", additional_options, body)
            RestUtil.map_attribute("token", additional_options, body)

        return RestUtil.execute_post(url, body, okta_headers)

    def authenticate_with_activation_token(self, token, headers=None):
        #self.logger.debug("OktaAuth.authenticate_with_activation_token()")
        url = "{host}/api/v1/authn".format(host=self.okta_config["okta_org_name"])
        okta_headers = OktaUtil.get_protected_okta_headers(self.okta_config)

        body = {
            "token": token
        }

        return RestUtil.execute_post(url, body, okta_headers)

    def get_transaction_state(self, token, headers=None):
        #self.logger.debug("OktaAuth.authenticate_with_activation_token()")
        url = "{host}/api/v1/authn".format(host=self.okta_config["okta_org_name"])
        okta_headers = OktaUtil.get_default_okta_headers(self.okta_config)

        body = {
            "stateToken": token
        }

        return RestUtil.execute_post(url, body, okta_headers)

    def reset_password_with_state_token(self, token, password, headers=None):
        #self.logger.debug("OktaAuth.reset_password_with_state_token()")
        url = "{host}/api/v1/authn/credentials/reset_password".format(host=self.okta_config["okta_org_name"])
        okta_headers = OktaUtil.get_protected_okta_headers(self.okta_config)

        body = {
            "stateToken": token,
            "newPassword": password
        }

        return RestUtil.execute_post(url, body, okta_headers)

    def create_oauth_authorize_url(self, response_type, state, auth_options):
        #self.logger.debug("OktaAuth.create_oauth_authorize_url()")

        url = (
            "{issuer}/v1/authorize?"
            "response_type={response_type}&"
            "client_id={clint_id}&"
            "redirect_uri={redirect_uri}&"
            "state={state}"
        ).format(
            issuer=self.okta_config["issuer"],
            clint_id=self.okta_config["client_id"],
            redirect_uri=self.okta_config["redirect_uri"],
            state=state,
            response_type=response_type
        )

        if auth_options:
            for key in auth_options:
                url = "{url}&{key}={value}".format(url=url, key=key, value=auth_options[key])

        return url

    def get_oauth_token(self, code, grant_type, auth_options=None, headers=None):
        #self.logger.debug("OktaAuth.get_oauth_token()")
        okta_headers = OktaUtil.get_oauth_okta_headers(headers, self.okta_config["client_id"], self.okta_config["client_secret"])

        url = (
            "{issuer}/v1/token?"
            "grant_type={grant_type}&"
            "code={code}&"
            "redirect_uri={redirect_uri}"
        ).format(
            issuer=self.okta_config["issuer"],
            code=code,
            redirect_uri=self.okta_config["redirect_uri"],
            grant_type=grant_type
        )

        body = {
            "authorization_code": code
        }

        if auth_options:
            for key in auth_options:
                url = "{url}&{key}={value}".format(url=url, key=key, value=auth_options[key])

        return RestUtil.execute_post(url, body, okta_headers)

    def introspect(self, token, headers=None):
        #self.logger.debug("OktaAuth.introspect()")
        okta_headers = OktaUtil.get_oauth_okta_headers(headers, self.okta_config["client_id"], self.okta_config["client_secret"])
        url = "{issuer}/v1/introspect?token={token}".format(
            issuer=self.okta_config["issuer"],
            token=token)
        body = {}
        return RestUtil.execute_post(url, body, okta_headers)

    def userinfo(self, token, headers=None):
        #self.logger.debug("OktaAuth.userinfo()")
        okta_headers = OktaUtil.get_oauth_okta_bearer_token_headers(token)

        url = "{issuer}/v1/userinfo?token={token}".format(
            issuer=self.okta_config["issuer"],
            token=token)
        body = {}

        return RestUtil.execute_post(url, body, okta_headers)

    """
    MFA verification methods
    """
    # used by Okta Verify Push, this starts the MFA transaction

    def send_push(self, factor_id, state_token, headers=None):
        #self.logger.debug("send_push()")
        okta_headers = OktaUtil.get_default_okta_headers(headers)

        url = "{0}/api/v1/authn/factors/{1}/verify".format(self.okta_config["okta_org_name"], factor_id)
        body = {
            "stateToken": state_token
        }

        return RestUtil.execute_post(url, body, okta_headers)

    # this is the Okta Verify Push polling method
    def poll_for_push(self, factor_id, state_token, headers=None):
        #self.logger.debug("poll_for_push()")
        okta_headers = OktaUtil.get_default_okta_headers(headers)

        url = "{0}/api/v1/authn/factors/{1}/verify".format(self.okta_config["okta_org_name"], factor_id)
        body = {
            "stateToken": state_token
        }
        return RestUtil.execute_post(url, body, okta_headers)

    def resend_push(self, factor_id, state_token, headers=None):
        #self.logger.debug("resend_push()")
        okta_headers = OktaUtil.get_default_okta_headers(headers)

        url = "{0}/api/v1/authn/factors/{1}/verify/resend".format(self.okta_config["okta_org_name"], factor_id)
        body = {
            "stateToken": state_token
        }

        return RestUtil.execute_post(url, body, okta_headers)

    # used by SMS, voice, Google Authenticator and Okta Verify OTP factors
    def verify_totp(self, factor_id, state_token, pass_code=None, headers=None):
        #self.logger.debug("verify_totp()")
        okta_headers = OktaUtil.get_default_okta_headers(headers)

        url = "{0}/api/v1/authn/factors/{1}/verify".format(self.okta_config["okta_org_name"], factor_id)
        body = {
            "stateToken": state_token,
            "passCode": pass_code
        }

        return RestUtil.execute_post(url, body, okta_headers)

    # used for Security Question factor
    def verify_answer(self, factor_id, state_token, answer, headers=None):
        #self.logger.debug("verify_answer()")
        okta_headers = OktaUtil.get_default_okta_headers(headers)

        url = "{0}/api/v1/authn/factors/{1}/verify".format(self.okta_config["okta_org_name"], factor_id)
        body = {
            "stateToken": state_token,
            "answer": answer
        }

        return RestUtil.execute_post(url, body, okta_headers)

    """
    end MFA verification methods
    """

    """
    MFA enrollment methods
    """
    # Okta Verify Push

    def enroll_push(self, state_token, factor_type, provider, headers=None):
        #self.logger.debug("enroll_push()")
        okta_headers = OktaUtil.get_default_okta_headers(headers)

        url = "{0}/api/v1/authn/factors".format(self.okta_config["okta_org_name"])
        body = {
            "stateToken": state_token,
            "factorType": factor_type,
            "provider": provider
        }

        return RestUtil.execute_post(url, body, okta_headers)

    # this is the Okta Verify Push polling method
    def poll_for_enrollment_push(self, factor_id, state_token, headers=None):
        #self.logger.debug("poll_for_enrollment_push()")
        okta_headers = OktaUtil.get_default_okta_headers(headers)

        url = "{0}/api/v1/authn/factors/{1}/lifecycle/activate/poll".format(
            self.okta_config["okta_org_name"],
            factor_id
        )
        body = {
            "stateToken": state_token
        }
        return RestUtil.execute_post(url, body, okta_headers)

    # this is the Okta Verify Push activation method
    def activate_push(self, factor_id, state_token, headers=None):
        #self.logger.debug("activate_push()")
        okta_headers = OktaUtil.get_default_okta_headers(headers)

        url = "{0}/api/v1/authn/factors/{1}/lifecycle/activate".format(
            self.okta_config["okta_org_name"],
            factor_id
        )
        body = {
            "stateToken": state_token
        }
        return RestUtil.execute_post(url, body, okta_headers)

    # Okta Verify OTP and Google Authenticator
    def enroll_totp(self, state_token, factor_type, provider, headers=None):
        #self.logger.debug("enroll_totp()")
        okta_headers = OktaUtil.get_default_okta_headers(headers)

        url = "{0}/api/v1/authn/factors".format(self.okta_config["okta_org_name"])
        body = {
            "stateToken": state_token,
            "factorType": factor_type,
            "provider": provider
        }

        return RestUtil.execute_post(url, body, okta_headers)

    # SMS and voice call
    def enroll_sms_voice(self, state_token, factor_type, provider, phone_number, headers=None):
        #self.logger.debug("enroll_sms_voice()")
        okta_headers = OktaUtil.get_default_okta_headers(headers)

        url = "{0}/api/v1/authn/factors".format(self.okta_config["okta_org_name"])
        body = {
            "stateToken": state_token,
            "factorType": factor_type,
            "provider": provider,
            "profile": {
                "phoneNumber": phone_number
            }
        }

        return RestUtil.execute_post(url, body, okta_headers)

    # security question
    def enroll_question(self, state_token, factor_type, provider, question, answer, headers=None):
        #self.logger.debug("enroll_question()")
        okta_headers = OktaUtil.get_default_okta_headers(headers)

        url = "{0}/api/v1/authn/factors".format(self.okta_config["okta_org_name"])
        body = {
            "stateToken": state_token,
            "factorType": factor_type,
            "provider": provider,
            "profile": {
                "question": question,
                "answer": answer
            }
        }

        return RestUtil.execute_post(url, body, okta_headers)

    # this is for Google Authenticator, SMS, and Voice factors
    def activate_totp(self, factor_id, state_token, pass_code, headers=None):
        #self.logger.debug("enroll_totp()")
        okta_headers = OktaUtil.get_default_okta_headers(headers)

        url = "{0}/api/v1/authn/factors/{1}/lifecycle/activate".format(
            self.okta_config["okta_org_name"],
            factor_id
        )
        body = {
            "stateToken": state_token,
            "passCode": pass_code
        }

        return RestUtil.execute_post(url, body, okta_headers)

    """
    end MFA enrollment methods
    """