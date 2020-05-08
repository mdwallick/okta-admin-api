import json
import os

from okta.util import OktaUtil
from okta.rest import RestUtil

class OktaFactors:

    okta_config = {
        "okta_org_name": os.getenv("OKTA_ORG_NAME"),
        "okta_api_token": os.getenv("OKTA_API_TOKEN")
    }

    def __init__(self):
        print("OktaFactors init()")
        #if okta_config:
        #    self.okta_config = okta_config
        #else:
        #    raise Exception("Requires okta_config")

    """
    MFA enrollment methods
    These are for enrollment outside of the authentication process
    """

    # Okta Verify Push
    def enroll_push(self, user_id):
        print("enroll_push()")
        okta_headers = OktaUtil.get_protected_okta_headers(self.okta_config)

        url = "{base_url}/api/v1/users/{user_id}/factors".format(
            base_url=self.okta_config["okta_org_name"],
            user_id=user_id
        )
        body = {
            "factorType": "push",
            "provider": "OKTA"
        }

        return RestUtil.execute_post(url, body, okta_headers)

    # send the push enrollment email
    # def enroll_push_send_activation_email(response, headers=None):
    #     okta_headers = OktaUtil.get_oauth_okta_bearer_token_headers
    #     links = response["_embedded"]["activation"]["_links"]["send"]
    #     #print("links: {0}".format(json.dumps(links, indent=2, sort_keys=True)))
    #     # do a POST to the email link
    #     url = links[0]["href"]
    #     print("POSTing to url {0}".format(url))
    #     RestUtil.execute_post(url)

    # this is the Okta Verify Push polling method
    def poll_for_enrollment_push(self, user_id, factor_id, headers=None):
        print("poll_for_enrollment_push()")
        okta_headers = OktaUtil.get_protected_okta_headers(self.okta_config)

        url = "{base_url}/api/v1/users/{user_id}/factors/{factor_id}/lifecycle/activate/poll".format(
            base_url=self.okta_config["okta_org_name"],
            user_id=user_id,
            factor_id=factor_id
        )
        body = {}

        return RestUtil.execute_post(url, body, okta_headers)

    def resend_push(self, user_id, factor_id, headers=None):
        print("resend_push()")
        okta_headers = OktaUtil.get_default_okta_headers(headers)

        url = "{base_url}/api/v1/users/{user_id}/factors/{factor_id}/lifecycle/activate".format(
            base_url=self.okta_config["okta_org_name"],
            user_id=user_id,
            factor_id=factor_id
        )
        body = {}

        return RestUtil.execute_post(url, body, okta_headers)

    # Okta Verify OTP (not push)
    def enroll_okta_verify_otp(self, user_id):
        print("enroll_okta_verify_otp")
        return self.__enroll_totp(user_id, "token:software:totp", "OKTA")

    # Google Authenticator
    def enroll_google_authenticator(self, user_id):
        print("enroll_google_authenticator")
        return self.__enroll_totp(user_id, "token:software:totp", "GOOGLE")

    # Okta Verify OTP and Google Authenticator
    def __enroll_totp(self, user_id, factor_type, provider):
        print("enroll_totp()")
        okta_headers = OktaUtil.get_protected_okta_headers(self.okta_config)

        url = "{base_url}/api/v1/users/{user_id}/factors".format(
            base_url=self.okta_config["okta_org_name"],
            user_id=user_id
        )
        body = {
            "factorType": factor_type,
            "provider": provider
        }

        return RestUtil.execute_post(url, body, okta_headers)

    # enroll SMS
    def enroll_sms(self, user_id, phone_number):
        print("enroll_sms()")
        return self.__enroll_sms_voice(user_id, phone_number, "sms", "OKTA")

    # enroll voice call
    def enroll_voice(self, user_id, phone_number):
        print("enroll_voice")
        return self.__enroll_sms_voice(user_id, phone_number, "call", "OKTA")

    # enroll email
    def enroll_email(self, user_id, email):
        print("enroll_email")
        okta_headers = OktaUtil.get_protected_okta_headers(self.okta_config)

        url = "{base_url}/api/v1/users/{user_id}/factors".format(
            base_url=self.okta_config["okta_org_name"],
            user_id=user_id
        )
        body = {
            "factorType": "email",
            "provider": "OKTA",
            "profile": {
                "email": email
            }
        }

        return RestUtil.execute_post(url, body, okta_headers)

    # SMS and voice call
    def __enroll_sms_voice(self, user_id, phone_number, factor_type, provider):
        print("__enroll_sms_voice()")
        okta_headers = OktaUtil.get_protected_okta_headers(self.okta_config)

        url = "{base_url}/api/v1/users/{user_id}/factors?updatePhone=true".format(
            base_url=self.okta_config["okta_org_name"],
            user_id=user_id
        )
        body = {
            "factorType": factor_type,
            "provider": provider,
            "profile": {
                "phoneNumber": phone_number
            }
        }

        return RestUtil.execute_post(url, body, okta_headers)

    # used by SMS, voice, Google Authenticator and Okta Verify OTP factors
    def activate_totp(self, user_id, factor_id, pass_code):
        print("verify_totp()")
        okta_headers = OktaUtil.get_protected_okta_headers(self.okta_config)

        url = "{base_url}/api/v1/users/{user_id}/factors/{factor_id}/lifecycle/activate".format(
            base_url=self.okta_config["okta_org_name"],
            user_id=user_id,
            factor_id=factor_id
        )
        body = {
            "passCode": pass_code
        }

        return RestUtil.execute_post(url, body, okta_headers)

    # security question
    def enroll_question(self, user_id, question, answer):
        print("enroll_question()")
        okta_headers = OktaUtil.get_protected_okta_headers(self.okta_config)

        url = "{base_url}/api/v1/users/{user_id}/factors".format(
            base_url=self.okta_config["okta_org_name"],
            user_id=user_id
        )
        body = {
            "factorType": "question",
            "provider": "OKTA",
            "profile": {
                "question": question,
                "answer": answer
            }
        }

        return RestUtil.execute_post(url, body, okta_headers)

    # lists factors that are active for the current user
    def list_enrolled_factors(self, user_id):
        print("list_enrolled_factors()")
        okta_headers = OktaUtil.get_protected_okta_headers(self.okta_config)

        url = "{base_url}/api/v1/users/{user_id}/factors".format(
            base_url=self.okta_config["okta_org_name"],
            user_id=user_id
        )

        return RestUtil.execute_get(url, okta_headers)

    # lists all possible factors (based on multifactor enrollment policy)
    # including active and inactive factors
    # this might be more useful to use to populate the UI
    # showing all factors regardless of status
    def list_available_factors(self, user_id):
        print("list_available_factors()")
        okta_headers = OktaUtil.get_protected_okta_headers(self.okta_config)

        url = "{base_url}/api/v1/users/{user_id}/factors/catalog".format(
            base_url=self.okta_config["okta_org_name"],
            user_id=user_id
        )

        return RestUtil.execute_get(url, okta_headers)

    def list_available_questions(self, user_id):
        print("list_available_questions()")
        okta_headers = OktaUtil.get_protected_okta_headers(self.okta_config)

        url = "{base_url}/api/v1/users/{user_id}/factors/questions".format(
            base_url=self.okta_config["okta_org_name"],
            user_id=user_id
        )

        return RestUtil.execute_get(url, okta_headers)

    def delete_factor(self, user_id, factor_id):
        print("delete_factor()")
        okta_headers = OktaUtil.get_protected_okta_headers(self.okta_config)

        url = "{base_url}/api/v1/users/{user_id}/factors/{factor_id}".format(
            base_url=self.okta_config["okta_org_name"],
            user_id=user_id,
            factor_id=factor_id
        )
        body = {}

        return RestUtil.execute_delete(url, body, okta_headers)
