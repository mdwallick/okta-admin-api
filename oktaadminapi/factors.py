# routes for the factors API endpoints
from flask import Blueprint, jsonify, make_response, request
from flask import current_app as app

from okta.FactorsClient import FactorsClient
from okta.framework.OktaError import OktaError
from okta.models.factor.Factor import Factor
from okta.models.factor.FactorEnrollRequest import FactorEnrollRequest

from oktaadminapi.decorators import authenticated

bp = Blueprint("factors", __name__)
client = FactorsClient(base_url=app.config.get("ORG_NAME"),
                       api_token=app.config.get("API_TOKEN"))


@authenticated
@bp.route("/<user_id>/factors/<factor_id>", methods=["GET"])
def get_factor(user_id, factor_id):
    """
    Gets a factor
    """
    app.logger.debug("get_factor({0}, {1})".format(user_id, factor_id))
    try:
        response = client.get_factor(user_id, factor_id)
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
@bp.route("/<user_id>/factors", methods=["GET"])
def get_enrolled_factors(user_id):
    """
    get enrolled factors
    """
    app.logger.debug("get_enrolled_factors({0})".format(user_id))
    try:
        response = client.get_lifecycle_factors(user_id)
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
@bp.route("/<user_id>/factors/catalog", methods=["GET"])
def get_available_factors(user_id):
    """
    get available factors
    """
    app.logger.debug("get_available_factors({0})".format(user_id))
    try:
        response = client.get_factors_catalog(user_id)
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
@bp.route("/<user_id>/factors/questions", methods=["GET"])
def get_available_questions(user_id):
    """
    get all available security questions
    """
    app.logger.debug("get_available_questions({0})".format(user_id))
    try:
        response = client.get_available_questions(user_id)
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
@bp.route("/<user_id>/factors/<factor_type>", methods=["POST"])
@bp.route("/<user_id>/factors/<factor_type>/<provider>", methods=["POST"])
def enroll_factor(user_id, factor_type, provider="OKTA"):
    """
    Main entry point for enrolling a factor

    Factor type must be one of:
    question
    sms
    call
    email
    totp (Google Authenticator or Okta Verify OTP)
    push

    provider must be one of
    Okta
    Google
    """
    provider = str(provider).upper()

    if factor_type == "totp":
        # map totp to the real factor type.
        # totp is just nicer in a URL
        factor_type = "token:software:totp"

    app.logger.debug("enroll_factor({0}, {1}, {2})".format(user_id, factor_type, provider))
    body = request.get_json()
    app.logger.info("got request body: {0}".format(body))

    if factor_type == "question":
        question = body.get("question")
        answer = body.get("answer")

        if not question or not answer:
            message = {
                "error_summary": "A question and answer are required"
            }
            return make_response(jsonify(message), 400)

        return enroll_question(user_id, question, answer)
    elif factor_type == "sms" or factor_type == "call":
        phone_number = body.get("phoneNumber")

        if not phone_number:
            message = {
                "error_summary": "A phone number is required"
            }
            return make_response(jsonify(message), 400)

        return enroll_phone_factor(user_id, factor_type, phone_number)
    elif factor_type == "email":
        email = body.get("email")

        if not email:
            message = {
                "error_summary": "An email address is required"
            }
            return make_response(jsonify(message), 400)

        return enroll_email(user_id, email)
    elif factor_type == "token:software:totp":
        if provider == "OKTA" or provider == "GOOGLE":
            return enroll_totp(user_id, provider)
        else:
            message = {
                "error_summary": "Provider must be one of Okta or Google"
            }
            return make_response(jsonify(message), 400)

    elif factor_type == "push":
        return enroll_push(user_id)
    else:
        error = "Factor type {0} is not supported".format(factor_type)
        message = {
            "error_summary": error
        }
        return make_response(jsonify(message), 400)


def __enroll_factor(user_id, enroll_request):
    try:
        response = client.enroll_factor(user_id, enroll_request)
        return jsonify(response)
    except OktaError as e:
        message = {
            "error_causes": e.error_causes,
            "error_summary": e.error_summary,
            "error_id": e.error_id,
            "error_code": e.error_code
        }
        return make_response(jsonify(message), e.status_code)


def enroll_question(user_id, question, answer):
    app.logger.debug("enroll_question({0}, {1}, ****)".format(user_id, question))
    enroll_request = {
        "factorType": "question",
        "provider": "OKTA",
        "profile": {
            "question": question,
            "answer": answer
        }
    }
    return __enroll_factor(user_id, enroll_request)


def enroll_phone_factor(user_id, factor_type, phone_number):
    app.logger.debug("enroll_sms({0}, {1})".format(user_id, phone_number))
    enroll_request = {
        "factorType": factor_type,
        "provider": "OKTA",
        "profile": {
            "phoneNumber": phone_number
        }
    }
    return __enroll_factor(user_id, enroll_request)


def enroll_email(user_id, email):
    app.logger.debug("enroll_email({0})".format(user_id))
    enroll_request = {
        "factorType": "email",
        "provider": "OKTA",
        "profile": {
            "email": email
        }
    }
    return __enroll_factor(user_id, enroll_request)


def enroll_totp(user_id, provider):
    """
    Enrolls Okta Verify OTP (not push) or Google Authenticator
    """
    app.logger.debug("enroll_totp({0}, {1})".format(user_id, provider))
    enroll_request = {
        "factorType": "token:software:totp",
        "provider": str(provider).upper()  # OKTA or GOOGLE
    }
    return __enroll_factor(user_id, enroll_request)


def enroll_push(user_id):
    app.logger.debug("enroll_push({0})".format(user_id))
    enroll_request = {
        "factorType": "push",
        "provider": "OKTA"
    }
    return __enroll_factor(user_id, enroll_request)


@authenticated
@bp.route("/<user_id>/factor/<factor_id>/activate/push", methods=["POST"])
def poll_push_activation(user_id, factor_id):
    app.logger.debug("poll_push_activation({0}, {1})".format(user_id, factor_id))
    body = request.get_json()
    poll_url = body.get("pollingUrl")
    try:
        response = client.push_activation_poll(poll_url)
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
    pass_code = body.get("passCode")
    try:
        response = client.activate_factor(user_id, factor_id, pass_code)
        return jsonify(response)
    except OktaError as e:
        message = {
            "error_causes": e.error_causes,
            "error_summary": e.error_summary,
            "error_id": e.error_id,
            "error_code": e.error_code
        }
        return make_response(jsonify(message), e.status_code)


"""
CHALLENGE/RESPONSE

sms
call
email

issue a challenge
/<user_id>/factor/<factor_id>/verify

verify a challenge
/<user_id>/factor/<factor_id>/verify
passCode in the body

PUSH
issue a challenge
/<user_id>/factor/<factor_id>/verify

POLL for response
/<user_id>/factor/<factor_id>/transactions/<transaction_id>

NO CHALLENGE, JUST A RESPONSE

question
/<user_id>/factor/<factor_id>/verify
answer in the body

TOTP (token:software:totp or token:hotp)
Token (token or token:hardware)
Yubikey (token:hardware)
/<user_id>/factor/<factor_id>/verify
passCode in the body

"""


@authenticated
@bp.route("/<user_id>/factor/<factor_id>/verify", methods=["POST"])
def verify_factor(user_id, factor_id):
    """
    Verify a factor challenge
    """
    answer = None
    pass_code = None
    body = request.get_json() or None

    try:
        if body is not None:
            if body.get("answer"):
                answer = body.get("answer")
                response = client.verify_factor(user_id, factor_id, answer=answer)
                return jsonify(response)
            elif body.get("passCode"):
                pass_code = body.get("passCode")
                response = client.verify_factor(user_id, factor_id, passcode=pass_code)
                return jsonify(response)
            else:
                message = {
                    "error_summary": "unknown parameters in request body",
                    "error_causes": jsonify(body)
                }
                return make_response(jsonify(message), 400)
        else:
            # no request body, start a challenge/response cycle
            response = client.verify_factor(user_id, factor_id)
            return jsonify(response)
    except OktaError as e:
        message = {
            "error_causes": e.error_causes,
            "error_summary": e.error_summary,
            "error_id": e.error_id,
            "error_code": e.error_code
        }
        return make_response(jsonify(message), e.status_code)
