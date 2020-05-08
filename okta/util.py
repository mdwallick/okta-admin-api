import base64
import os

class OktaUtil:

    @staticmethod
    def get_default_okta_headers(headers):
        okta_default_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        return okta_default_headers

    @staticmethod
    def get_protected_okta_headers(okta_config):
        okta_api_token = okta_config["okta_api_token"]
        okta_protected_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "SSWS {0}".format(okta_api_token)
        }

        return okta_protected_headers

    @staticmethod
    def get_oauth_okta_headers(headers, client_id, client_secret=None):
        okta_oauth_headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        if client_id and client_secret:
            okta_oauth_headers["Authorization"] = "Basic {0}".format(OktaUtil.get_encoded_auth(client_id, client_secret))
        else:
            okta_oauth_headers["Authorization"] = "Basic {0}".format(OktaUtil.get_encoded_auth(client_id))
            
        return okta_oauth_headers

    @staticmethod
    #def get_oauth_okta_bearer_token_headers(headers, token):
    def get_oauth_okta_bearer_token_headers(token):
        okta_oauth_headers = {"Authorization": "Bearer {0}".format(token)}

        return okta_oauth_headers

    @staticmethod
    def get_encoded_auth(client_id, client_secret=None):
        if client_secret != None:
            auth_raw = "{client_id}:{client_secret}".format(
                client_id=client_id,
                client_secret=client_secret
            )
        else:
            auth_raw = "{client_id}".format(
                client_id=client_id
            )

        encoded_auth = base64.b64encode(bytes(auth_raw, 'UTF-8')).decode("UTF-8")

        return encoded_auth