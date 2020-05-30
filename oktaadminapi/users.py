# routes for the user API endpoints
# TODO implement the rest of the user API endpoints
#       get_paged_users

from flask import Blueprint, jsonify, make_response, request
from flask import current_app as app

from okta.framework.OktaError import OktaError
from okta.UsersClient import UsersClient
from okta.models.user.User import User

from oktaadminapi.decorators import authenticated
from oktaadminapi.okta_class_extensions import ExtendedUser

bp = Blueprint("users", __name__)
client = UsersClient(base_url=app.config.get("ORG_NAME"),
                     api_token=app.config.get("API_TOKEN"),
                     user_class=ExtendedUser)


@authenticated
@bp.route("/<user_id>", methods=["GET"])
def get_user(user_id):
    """ get a user """
    app.logger.debug("get_user({0})".format(user_id))
    try:
        response = client.get_user(user_id)
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
@bp.route("", methods=["GET"])
def get_users():
    """
    Gets a list of users

    :param limit: maximum number of users to return
    :type limit: int or None
    :param query: string to search users' first names, last names, and emails
    :type query: str or None
    :param filter_string: string to filter users by status, lastUpdated, id, 
    profile.login, profile.email, profile.firstName, and profile.lastName
    :type filter_string: str or None
    :rtype: list of User
    """
    app.logger.debug("get_users()")
    for item in request.args.items():
        app.logger.debug("argument: {0}".format(item))

    limit = request.args.get("limit") or None
    query = request.args.get("query") or None
    filter_string = request.args.get("filter") or None
    try:
        response = client.get_users(limit=limit, query=query, filter_string=filter_string)
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
@bp.route("/<user_id>/appLinks", methods=["GET"])
def get_user_applinks(user_id):
    """ get a user's application links """
    app.logger.debug("get_user_applinks({0})".format)
    try:
        response = client.get_user_applinks(user_id)
        return jsonify(response)
    except OktaError as e:
        message = {
            "error_causes": e.error_causes,
            "error_summary": e.error_summary,
            "error_id": e.error_id,
            "error_code": e.error_code
        }
        return make_response(jsonify(message), e.status_code)


# leave the url string empty if you just want to use
# the blueprint's base URL, e.g. /api/v1/users


@authenticated
@bp.route("", methods=["POST"])
def create_user():
    """ create a user """
    app.logger.debug("create_user()")
    user = request.get_json()
    activate = str(request.args.get("activate")).lower()
    if activate == "false":
        activate = False
    else:
        activate = True

    try:
        response = client.create_user(user, activate)
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
@bp.route("/<user_id>", methods=["PUT"])
def update_user(user_id):
    """ update a user """
    app.logger.debug("update_user({0})".format(user_id))
    user = request.get_json()
    try:
        response = client.update_user_by_id(user_id, user)
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
@bp.route("/<user_id>/credentials/change_password", methods=["POST"])
def change_password(user_id):
    """
    Change a user's password by verifying the current password
    """
    app.logger.debug("change_password({0})".format(user_id))
    body = request.get_json()
    old_password = body["oldPassword"] or None
    new_password = body["newPassword"] or None
    try:
        response = client.change_password(user_id, old_password, new_password)
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
@bp.route("/<user_id>/lifecycle/expire_password", methods=["POST"])
def expire_password(user_id):
    """
    Sets a user's password to expired so they
    must change it on next login
    """
    temp_password = (request.args.get("tempPassword") == True) or False
    app.logger.debug("expire_password({0})".format(user_id))
    try:
        response = client.expire_password(user_id, temp_password)
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
@bp.route("/<user_id>/lifecycle/reset_password", methods=["POST"])
def reset_password(user_id):
    """
    Resets a user's password and emails a reset password link.
    """
    send_email = (request.args.get("sendEmail") == True) or False
    app.logger.debug("reset_password({0})".format(user_id))
    try:
        response = client.reset_password(user_id, send_email)
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
@bp.route("/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    """
    Deletes a user

    In its current implementation, this needs to be called
    twice to actually delete the user. The first call just
    deactivates the user
    """
    app.logger.debug("delete_user({0})".format(user_id))
    try:
        response = client.delete_user(user_id)
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
@bp.route("/<user_id>/lifecycle/activate", methods=["POST"])
def activate_user(user_id):
    """
    Activates a user
    """
    app.logger.debug("activate_user({0})".format(user_id))
    send_email = str(request.args.get("sendEmail")).lower()
    if send_email == "false":
        send_email = False
    else:
        send_email = True

    try:
        response = client.activate_user(user_id, send_email)
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
@bp.route("/<user_id>/lifecycle/deactivate", methods=["POST"])
def deactivate_user(user_id):
    """
    Deactivates a user
    """
    app.logger.debug("deactivate_user({0}".format(user_id))
    try:
        response = client.deactivate_user(user_id)
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
@bp.route("/<user_id>/lifecycle/suspend", methods=["POST"])
def suspend_user(user_id):
    """
    Suspends a user
    """
    app.logger.debug("suspend_user({0}".format(user_id))
    try:
        response = client.suspend_user(user_id)
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
@bp.route("/<user_id>/lifecycle/unsuspend", methods=["POST"])
def unsuspend_user(user_id):
    """
    Unsuspends a user
    """
    app.logger.debug("unsuspend_user({0}".format(user_id))
    try:
        response = client.unsuspend_user(user_id)
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
@bp.route("/<user_id>/lifecycle/unlock", methods=["POST"])
def unlock_user(user_id):
    """
    Unlocks a user
    """
    app.logger.debug("unlock_user({0}".format(user_id))
    try:
        response = client.unlock_user(user_id)
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
@bp.route("/<user_id>/lifecycle/reset_factors", methods=["POST"])
def reset_factors(user_id):
    """
    Resets all factors for the given user
    """
    app.logger.debug("reset_factors({0}".format(user_id))
    try:
        response = client.reset_factors(user_id)
        return jsonify(response)
    except OktaError as e:
        message = {
            "error_causes": e.error_causes,
            "error_summary": e.error_summary,
            "error_id": e.error_id,
            "error_code": e.error_code
        }
        return make_response(jsonify(message), e.status_code)
