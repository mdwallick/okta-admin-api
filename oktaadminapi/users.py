from flask import Blueprint, jsonify, make_response, request
from flask import current_app as app
from flask_api import status

from okta.framework.OktaError import OktaError
from okta.framework.Serializer import Serializer
from okta.UsersClient import UsersClient
from okta.models.user.User import User

from oktaadminapi.decorators import authenticated

bp = Blueprint("users", __name__)

# CRUD operations


@bp.route("/<user_id>", methods=["GET"])
@authenticated
def get_user(user_id):
    """ get a user """
    app.logger.debug("get_user({0})".format(user_id))
    try:
        response = app.usersClient.get_user(user_id)
        return jsonify(response)
    except OktaError as e:
        message = {
            "error_causes": e.error_causes,
            "error_summary": e.error_summary,
            "error_id": e.error_id,
            "error_code": e.error_code
        }
        return make_response(jsonify(message), e.status_code)


@bp.route("", methods=["GET"])
@authenticated
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
        response = app.usersClient.get_users(limit=limit, query=query, filter_string=filter_string)
        return jsonify(response)
    except OktaError as e:
        message = {
            "error_causes": e.error_causes,
            "error_summary": e.error_summary,
            "error_id": e.error_id,
            "error_code": e.error_code
        }
        return make_response(jsonify(message), e.status_code)


@bp.route("/search", methods=["GET"])
@authenticated
def get_paged_users():
    limit = request.args.get("limit") or None
    filter_string = request.args.get("filter") or None
    after = request.args.get("after") or None
    url = request.args.get("url") or None
    try:
        if url != None:
            response = app.usersClient.get_paged_users(url=url)
        else:
            response = app.usersClient.get_paged_users(limit=limit, filter_string=filter_string, after=after)

        resp = make_response(jsonify(response.result), status.HTTP_200_OK)
        resp.headers["Link"] = "<{0}>; rel=\"next\"".format(response.next_url)
        return resp
    except OktaError as e:
        message = {
            "error_causes": e.error_causes,
            "error_summary": e.error_summary,
            "error_id": e.error_id,
            "error_code": e.error_code
        }
        return make_response(jsonify(message), e.status_code)


@bp.route("", methods=["POST"])
@authenticated
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
        response = app.usersClient.create_user(user, activate)
        return jsonify(response)
    except OktaError as e:
        message = {
            "error_causes": e.error_causes,
            "error_summary": e.error_summary,
            "error_id": e.error_id,
            "error_code": e.error_code
        }
        return make_response(jsonify(message), e.status_code)


@bp.route("/<user_id>", methods=["PUT"])
@authenticated
def update_user(user_id):
    """ update a user """
    app.logger.debug("update_user({0})".format(user_id))
    user = request.get_json()
    try:
        response = app.usersClient.update_user_by_id(user_id, user)
        return jsonify(response)
    except OktaError as e:
        message = {
            "error_causes": e.error_causes,
            "error_summary": e.error_summary,
            "error_id": e.error_id,
            "error_code": e.error_code
        }
        return make_response(jsonify(message), e.status_code)


@bp.route("/<user_id>", methods=["DELETE"])
@authenticated
def delete_user(user_id):
    """
    Deletes a user

    In its current implementation, this needs to be called
    twice to actually delete the user. The first call just
    deactivates the user
    """
    app.logger.debug("delete_user({0})".format(user_id))
    try:
        response = app.usersClient.delete_user(user_id)
        return jsonify(response)
    except OktaError as e:
        message = {
            "error_causes": e.error_causes,
            "error_summary": e.error_summary,
            "error_id": e.error_id,
            "error_code": e.error_code
        }
        return make_response(jsonify(message), e.status_code)


# related operations

@bp.route("/<user_id>/appLinks", methods=["GET"])
@authenticated
def get_user_applinks(user_id):
    """ get a user's application links """
    app.logger.debug("get_user_applinks({0})".format)
    try:
        response = app.usersClient.get_user_applinks(user_id)
        return jsonify(response)
    except OktaError as e:
        message = {
            "error_causes": e.error_causes,
            "error_summary": e.error_summary,
            "error_id": e.error_id,
            "error_code": e.error_code
        }
        return make_response(jsonify(message), e.status_code)


@bp.route("/<user_id>/groups", methods=["GET"])
@authenticated
def get_user_groups(user_id):
    """ get the groups a user belongs to """
    app.logger.debug("get_user_groups({0})".format(user_id))
    try:
        response = app.usersClient.get_user_groups(user_id)
        return jsonify(response)
    except OktaError as e:
        message = {
            "error_causes": e.error_causes,
            "error_summary": e.error_summary,
            "error_id": e.error_id,
            "error_code": e.error_code
        }
        return make_response(jsonify(message), e.status_code)


# credential operations

@bp.route("/<user_id>/credentials/forgot_password", methods=["POST"])
@authenticated
def forgot_password(user_id):
    """ starts the forgot password flow """
    message = {
        "error_summary": "Method not yet implemented"
    }
    return make_response(jsonify(message), status.HTTP_400_BAD_REQUEST)


@bp.route("/<user_id>/credentials/change_password", methods=["POST"])
@authenticated
def change_password(user_id):
    """
    Change a user's password by verifying the current password
    """
    app.logger.debug("change_password({0})".format(user_id))
    body = request.get_json()
    old_password = body["oldPassword"] or None
    new_password = body["newPassword"] or None
    try:
        response = app.usersClient.change_password(user_id, old_password, new_password)
        return jsonify(response)
    except OktaError as e:
        message = {
            "error_causes": e.error_causes,
            "error_summary": e.error_summary,
            "error_id": e.error_id,
            "error_code": e.error_code
        }
        return make_response(jsonify(message), e.status_code)


@bp.route("/<user_id>/credentials/change_recovery_question", methods=["POST"])
@authenticated
def change_recovery_question(user_id):
    """
    Change a user's password by verifying the current password
    """
    app.logger.debug("change_password({0})".format(user_id))
    # body = request.get_json()
    # password = body["password"] or None
    # recovery_question = body["recovery_question"] or None
    message = {
        "error_summary": "Method not yet implemented"
    }
    return make_response(jsonify(message), status.HTTP_400_BAD_REQUEST)


# lifecycle operations

@bp.route("/<user_id>/lifecycle/expire_password", methods=["POST"])
@authenticated
def expire_password(user_id):
    """
    Sets a user's password to expired so they
    must change it on next login
    """
    temp_password = (request.args.get("tempPassword") == True) or False
    app.logger.debug("expire_password({0})".format(user_id))
    try:
        response = app.usersClient.expire_password(user_id, temp_password)
        return jsonify(response)
    except OktaError as e:
        message = {
            "error_causes": e.error_causes,
            "error_summary": e.error_summary,
            "error_id": e.error_id,
            "error_code": e.error_code
        }
        return make_response(jsonify(message), e.status_code)


@bp.route("/<user_id>/lifecycle/reset_password", methods=["POST"])
@authenticated
def reset_password(user_id):
    """
    Resets a user's password and emails a reset password link.
    """
    send_email = (request.args.get("sendEmail") == True) or False
    app.logger.debug("reset_password({0})".format(user_id))
    try:
        response = app.usersClient.reset_password(user_id, send_email)
        return jsonify(response)
    except OktaError as e:
        message = {
            "error_causes": e.error_causes,
            "error_summary": e.error_summary,
            "error_id": e.error_id,
            "error_code": e.error_code
        }
        return make_response(jsonify(message), e.status_code)


@bp.route("/<user_id>/lifecycle/activate", methods=["POST"])
@authenticated
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
        response = app.usersClient.activate_user(user_id, send_email)
        return jsonify(response)
    except OktaError as e:
        message = {
            "error_causes": e.error_causes,
            "error_summary": e.error_summary,
            "error_id": e.error_id,
            "error_code": e.error_code
        }
        return make_response(jsonify(message), e.status_code)


@bp.route("/<user_id>/lifecycle/deactivate", methods=["POST"])
@authenticated
def deactivate_user(user_id):
    """
    Deactivates a user
    """
    app.logger.debug("deactivate_user({0}".format(user_id))
    try:
        response = app.usersClient.deactivate_user(user_id)
        return jsonify(response)
    except OktaError as e:
        message = {
            "error_causes": e.error_causes,
            "error_summary": e.error_summary,
            "error_id": e.error_id,
            "error_code": e.error_code
        }
        return make_response(jsonify(message), e.status_code)


@bp.route("/<user_id>/lifecycle/suspend", methods=["POST"])
@authenticated
def suspend_user(user_id):
    """
    Suspends a user
    """
    app.logger.debug("suspend_user({0}".format(user_id))
    try:
        response = app.usersClient.suspend_user(user_id)
        return jsonify(response)
    except OktaError as e:
        message = {
            "error_causes": e.error_causes,
            "error_summary": e.error_summary,
            "error_id": e.error_id,
            "error_code": e.error_code
        }
        return make_response(jsonify(message), e.status_code)


@bp.route("/<user_id>/lifecycle/unsuspend", methods=["POST"])
@authenticated
def unsuspend_user(user_id):
    """
    Unsuspends a user
    """
    app.logger.debug("unsuspend_user({0}".format(user_id))
    try:
        response = app.usersClient.unsuspend_user(user_id)
        return jsonify(response)
    except OktaError as e:
        message = {
            "error_causes": e.error_causes,
            "error_summary": e.error_summary,
            "error_id": e.error_id,
            "error_code": e.error_code
        }
        return make_response(jsonify(message), e.status_code)


@bp.route("/<user_id>/lifecycle/unlock", methods=["POST"])
@authenticated
def unlock_user(user_id):
    """
    Unlocks a user
    """
    app.logger.debug("unlock_user({0}".format(user_id))
    try:
        response = app.usersClient.unlock_user(user_id)
        return jsonify(response)
    except OktaError as e:
        message = {
            "error_causes": e.error_causes,
            "error_summary": e.error_summary,
            "error_id": e.error_id,
            "error_code": e.error_code
        }
        return make_response(jsonify(message), e.status_code)


@bp.route("/<user_id>/lifecycle/reset_factors", methods=["POST"])
@authenticated
def reset_factors(user_id):
    """
    Resets all factors for the given user
    """
    app.logger.debug("reset_factors({0}".format(user_id))
    try:
        response = app.usersClient.reset_factors(user_id)
        return jsonify(response)
    except OktaError as e:
        message = {
            "error_causes": e.error_causes,
            "error_summary": e.error_summary,
            "error_id": e.error_id,
            "error_code": e.error_code
        }
        return make_response(jsonify(message), e.status_code)
