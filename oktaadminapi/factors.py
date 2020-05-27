# routes for the factors API endpoints
from flask import Blueprint, jsonify, make_response, request
from flask import current_app as app

from okta.FactorsClient import FactorsClient
from okta.framework.OktaError import OktaError
from okta.models.factor.Factor import Factor
from okta.models.factor.FactorEnrollRequest import FactorEnrollRequest

from oktaadminapi.decorators import authenticated

bp = Blueprint("factors", __name__)
factorsClient = FactorsClient(base_url=app.config.get("ORG_NAME"),
                              api_token=app.config.get("API_TOKEN"))


@bp.route("/<user_id>", methods=["GET"])
@authenticated
def get_enrolled_factors(user_id):
    """
    get enrolled factors
    """
    app.logger.debug("get_enrolled_factors({0})".format(user_id))
    try:
        response = factorsClient.get_lifecycle_factors(user_id)
        return jsonify(response)
    except OktaError as e:
        message = {
            "error_causes": e.error_causes,
            "error_summary": e.error_summary,
            "error_id": e.error_id,
            "error_code": e.error_code
        }
        return make_response(jsonify(message), e.status_code)


@bp.route("/<user_id>/available", methods=["GET"])
@authenticated
def get_available_factors(user_id):
    """
    get available factors
    """
    app.logger.debug("get_available_factors({0})".format(user_id))
    try:
        response = factorsClient.get_factors_catalog(user_id)
        return jsonify(response)
    except OktaError as e:
        message = {
            "error_causes": e.error_causes,
            "error_summary": e.error_summary,
            "error_id": e.error_id,
            "error_code": e.error_code
        }
        return make_response(jsonify(message), e.status_code)


@bp.route("/<user_id>/available/questions", methods=["GET"])
@authenticated
def get_available_questions(user_id):
    """
    get all available security questions
    """
    app.logger.debug("get_available_questions({0})".format(user_id))
    try:
        response = factorsClient.get_available_questions(user_id)
        return jsonify(response)
    except OktaError as e:
        message = {
            "error_causes": e.error_causes,
            "error_summary": e.error_summary,
            "error_id": e.error_id,
            "error_code": e.error_code
        }
        return make_response(jsonify(message), e.status_code)


@bp.route("/<user_id>/enroll/question", methods=["POST"])
@authenticated
def enroll_question(user_id):
    app.logger.debug("enroll_question({0})".format(user_id))
    body = request.get_json()
    question = body["question"]
    answer = body["answer"]
    enroll_request = {
        "factorType": "question",
        "provider": "OKTA",
        "profile": {
            "question": question,
            "answer": answer
        }
    }
    try:
        response = factorsClient.enroll_factor(user_id, enroll_request)
        return jsonify(response)
    except OktaError as e:
        message = {
            "error_causes": e.error_causes,
            "error_summary": e.error_summary,
            "error_id": e.error_id,
            "error_code": e.error_code
        }
        return make_response(jsonify(message), e.status_code)


@authenticated
@bp.route("/<user_id>/enroll/sms", methods=["POST"])
def enroll_sms(user_id):
    app.logger.debug("enroll_sms({0})".format(user_id))
    body = request.get_json()
    phone_number = body["phoneNumber"]
    enroll_request = {
        "factorType": "sms",
        "provider": "OKTA",
        "profile": {
            "phoneNumber": phone_number
        }
    }
    try:
        response = factorsClient.enroll_factor(user_id, enroll_request, True)
        return jsonify(response)
    except OktaError as e:
        message = {
            "error_causes": e.error_causes,
            "error_summary": e.error_summary,
            "error_id": e.error_id,
            "error_code": e.error_code
        }
        return make_response(jsonify(message), e.status_code)


@authenticated
@bp.route("/<user_id>/enroll/voice", methods=["POST"])
def enroll_voice(user_id):
    app.logger.debug("enroll_voice({0})".format(user_id))
    body = request.get_json()
    phone_number = body["phoneNumber"]
    enroll_request = {
        "factorType": "call",
        "provider": "OKTA",
        "profile": {
            "phoneNumber": phone_number
        }
    }
    try:
        response = factorsClient.enroll_factor(user_id, enroll_request, True)
        return jsonify(response)
    except OktaError as e:
        message = {
            "error_causes": e.error_causes,
            "error_summary": e.error_summary,
            "error_id": e.error_id,
            "error_code": e.error_code
        }
        return make_response(jsonify(message), e.status_code)


@authenticated
@bp.route("/<user_id>/enroll/email", methods=["POST"])
def enroll_email(user_id):
    app.logger.debug("enroll_email({0})".format(user_id))
    body = request.get_json()
    email = body["email"]
    enroll_request = {
        "factorType": "email",
        "provider": "OKTA",
        "profile": {
            "email": email
        }
    }
    try:
        response = factorsClient.enroll_factor(user_id, enroll_request, True)
        return jsonify(response)
    except OktaError as e:
        message = {
            "error_causes": e.error_causes,
            "error_summary": e.error_summary,
            "error_id": e.error_id,
            "error_code": e.error_code
        }
        return make_response(jsonify(message), e.status_code)


@authenticated
@bp.route("/<user_id>/enroll/totp/<provider>", methods=["POST"])
def enroll_totp(user_id, provider):
    """
    Enrolls Okta Verify OTP (not push) or Google Authenticator
    """
    app.logger.debug("enroll_totp({0}, {1})".format(user_id, provider))
    enroll_request = {
        "factorType": "token:software:totp",
        "provider": str(provider).upper() # OKTA or GOOGLE
    }
    try:
        response = factorsClient.enroll_factor(user_id, enroll_request, True)
        return jsonify(response)
    except OktaError as e:
        message = {
            "error_causes": e.error_causes,
            "error_summary": e.error_summary,
            "error_id": e.error_id,
            "error_code": e.error_code
        }
        return make_response(jsonify(message), e.status_code)


@authenticated
@bp.route("/<user_id>/factor/<factor_id>/activate/totp", methods=["POST"])
def activate_totp(user_id, factor_id):
    """
    Activate SMS, voice, Google Authenticator or email factors
    """
    app.logger.debug("activate_totp({0}, {1})".format(user_id, factor_id))
    body = request.get_json()
    pass_code = body["passCode"]
    try:
        response = factorsClient.activate_factor(user_id, factor_id, pass_code)
        return jsonify(response)
    except OktaError as e:
        message = {
            "error_causes": e.error_causes,
            "error_summary": e.error_summary,
            "error_id": e.error_id,
            "error_code": e.error_code
        }
        return make_response(jsonify(message), e.status_code)

# @bp.route("/enroll/push", methods=["POST"])
# @authenticated
# def enroll_push():
#     logger.debug("enroll_push()")
#     okta_factors = OktaFactors()
#     user_id = get_userid_from_token()
#     response = okta_factors.enroll_push(user_id)
#     factor_id = response["id"]
#     logger.info("Factor with ID {0} pending activation".format(factor_id))
#     # take the response and send it off to have the activation link emailed
#     #enroll_push_send_activation_email(response)
#     return response

# # take the response from enrolling the push and email the link out
# def enroll_push_send_activation_email(response):
#     logger.debug("enroll_push_send_activation_email()")
#     links = response["_embedded"]["activation"]["_links"]["send"]
#     logger.debug("links: {0}".format(json.dumps(links, indent=2, sort_keys=True)))
#     # do a POST to the email link
#     access_token = get_access_token()
#     headers = OktaUtil.get_oauth_okta_bearer_token_headers(access_token)
#     body = {}
#     url = links[0]["href"]
#     logger.debug("POSTing to url {0}".format(url))
#     RestUtil.execute_post(url, body, headers)
