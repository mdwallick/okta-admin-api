import base64
import os
import config
import json
import time

from flask import Flask, abort, jsonify, request, make_response
from flask_cors import CORS
from functools import wraps

from okta.auth import OktaAuth
from okta.admin import OktaAdmin
from okta.factors import OktaFactors
from okta.util import OktaUtil
from okta.rest import RestUtil

"""
GLOBAL VARIABLES ########################################################################################################
"""
app = Flask(__name__)
app.secret_key = "6w_#w*~AVts3!*yd&C]jP0(x_1ssd]MVgzfAw8%fF+c@|ih0s1H&yZQC&-u~O[--"  # For the session
CORS(app)

@app.errorhandler(401)
def not_authorized(error):
    message = {
        "error": "Unauthorized",
        "message": "Invalid, expired or missing bearer token"
    }
    return make_response(jsonify(message), 401)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)


"""
function decorators
"""
def authenticated(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        print("authenticated()")

        # Just validate they have a legit token. Any additional access rules will be by another wrapper
        access_token = get_access_token()
        if is_token_valid_remote(access_token):
            return f(*args, **kws)
        else:
            abort(401)

    return decorated_function

def get_access_token():
    access_token = None
    authorization_header = request.headers.get("authorization")
    print("Authorization header {0}".format(authorization_header))

    if authorization_header != None:
        header = "Bearer"
        bearer, access_token = authorization_header.split(" ")
        #print("{0}: {1}".format(bearer, access_token))
        if bearer != header:
            abort(401)

    return access_token

def is_token_valid_remote(token):
    print("is_token_valid_remote(token)")
    result = False

    okta_auth = OktaAuth()
    introspect_response = okta_auth.introspect(token=token)
    #print("introspect_response: {0}".format(introspect_response))

    if "active" in introspect_response:
        result = introspect_response["active"]

    return result

def get_claims_from_token():
    print("get_claims_from_token(token)")
    token = get_access_token()
    claims = None

    if token:
        jwt = token.encode("utf-8")
        token_payload = jwt.decode().split(".")[1]
        claims_string = decode_base64(token_payload)
        claims = json.loads(claims_string)

    return claims

def get_userid_from_token():
    claims = get_claims_from_token()
    return claims["uid"]

def decode_base64(data):
    missing_padding = len(data) % 4
    if missing_padding > 0:
        data += "=" * (4 - missing_padding)
    return base64.urlsafe_b64decode(data)


"""
ROUTES ##################################################################################################################
"""

"""
TODO implement endpoints for user profile updates and self-service factor management
"""

# get user
@app.route("/api/v1/user", methods=["GET"])
@authenticated
def get_user():
    print("get_user")
    okta_admin = OktaAdmin()
    user_id = get_userid_from_token()
    return okta_admin.get_user(user_id)

# update user
@app.route("/api/v1/user", methods=["POST"])
@authenticated
def update_user():
    print("update_user")
    okta_admin = OktaAdmin()
    user_id = get_userid_from_token()
    user = request.get_json()
    return okta_admin.update_user(user_id, user)

# get enrolled factors
@app.route("/api/v1/factors", methods=["GET"])
@authenticated
def get_enrolled_factors():
    print("get_enrolled_factors()")
    okta_factors = OktaFactors()
    user_id = get_userid_from_token()
    response = okta_factors.list_enrolled_factors(user_id)
    return jsonify(response)

# get available factors
@app.route("/api/v1/factors/available", methods=["GET"])
@authenticated
def get_available_factors():
    print("get_available_factors()")
    okta_factors = OktaFactors()
    user_id = get_userid_from_token()
    response = okta_factors.list_available_factors(user_id)
    return jsonify(response)

# get all available security questions
@app.route("/api/v1/factors/available/questions", methods=["GET"])
@authenticated
def get_available_questions():
    print("get_available_questions()")
    okta_factors = OktaFactors()
    user_id = get_userid_from_token()
    response = okta_factors.list_available_questions(user_id)
    return jsonify(response)

@app.route("/api/v1/factors/enroll/question", methods=["POST"])
@authenticated
def enroll_question():
    print("enroll_question()")
    okta_factors = OktaFactors()
    user_id = get_userid_from_token()
    body = request.get_json()
    question = body["question"]
    answer = body["answer"]
    response = okta_factors.enroll_question(user_id, question, answer)
    return response

@app.route("/api/v1/factors/enroll/sms", methods=["POST"])
@authenticated
def enroll_sms():
    print("enroll_sms()")
    okta_factors = OktaFactors()
    user_id = get_userid_from_token()
    body = request.get_json()
    phone_number = body["phone_number"]
    response = okta_factors.enroll_sms(user_id, phone_number)
    factor_id = response["id"]
    print("Factor with ID {0} pending activation".format(factor_id))
    return response

@app.route("/api/v1/factors/enroll/voice", methods=["POST"])
@authenticated
def enroll_voice():
    print("enroll_voice()")
    okta_factors = OktaFactors()
    user_id = get_userid_from_token()
    body = request.get_json()
    phone_number = body["phone_number"]
    response = okta_factors.enroll_voice(user_id, phone_number)
    factor_id = response["id"]
    print("Factor with ID {0} pending activation".format(factor_id))
    return response

@app.route("/api/v1/factors/enroll/email", methods=["POST"])
@authenticated
def enroll_email():
    print("enroll_email()")
    okta_factors = OktaFactors()
    user_id = get_userid_from_token()
    body = request.get_json()
    email = body["email"]
    response = okta_factors.enroll_email(user_id, email)
    factor_id = response["id"]
    print("Factor with ID {0} pending activation".format(factor_id))
    return response

@app.route("/api/v1/factors/activate/totp", methods=["POST"])
@authenticated
def activate_totp():
    print("activate_totp()")
    okta_factors = OktaFactors()
    user_id = get_userid_from_token()
    body = request.get_json()
    factor_id = body["factor_id"]
    pass_code = body["passCode"]
    return okta_factors.activate_totp(user_id, factor_id, pass_code)

# @app.route("/api/v1/factors/enroll/push", methods=["POST"])
# @authenticated
# def enroll_push():
#     print("enroll_push()")
#     okta_factors = OktaFactors()
#     user_id = get_userid_from_token()
#     response = okta_factors.enroll_push(user_id)
#     factor_id = response["id"]
#     print("Factor with ID {0} pending activation".format(factor_id))
#     # take the response and send it off to have the activation link emailed
#     #enroll_push_send_activation_email(response)
#     return response

# take the response from enrolling the push and email the link out
# def enroll_push_send_activation_email(response):
#     print("enroll_push_send_activation_email()")
#     links = response["_embedded"]["activation"]["_links"]["send"]
#     print("links: {0}".format(json.dumps(links, indent=2, sort_keys=True)))
#     # do a POST to the email link
#     access_token = get_access_token()
#     headers = OktaUtil.get_oauth_okta_bearer_token_headers(access_token)
#     body = {}
#     url = links[0]["href"]
#     print("POSTing to url {0}".format(url))
#     RestUtil.execute_post(url, body, headers)


"""
MAIN ##################################################################################################################
"""
if __name__ == "__main__":
    # This is to run on c9.io.. you may need to change or make your own runner
    #print("okta_config: {0}".format(json.dumps(okta_settings, indent=4, sort_keys=True)))
    app.run(host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 3000)))