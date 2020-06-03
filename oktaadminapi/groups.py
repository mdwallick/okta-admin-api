# routes for the group API endpoints
# TODO implement the rest of the group API endpoints
#       get_paged_groups

from flask import Blueprint, jsonify, make_response, request
from flask import current_app as app

from okta.framework.OktaError import OktaError
from okta.UserGroupsClient import UserGroupsClient
from okta.models.usergroup import UserGroup
from oktaadminapi.decorators import authenticated

bp = Blueprint("groups", __name__)
client = UserGroupsClient(base_url=app.config.get("ORG_NAME"),
                          api_token=app.config.get("API_TOKEN"))


@bp.route("/<group_id>", methods=["GET"])
@authenticated
def get_group(group_id):
    """ get a group """
    app.logger.debug("get_group({0})".format(group_id))
    try:
        response = client.get_group(group_id)
        return jsonify(response)
    except OktaError as e:
        message = {
            "error_causes": e.error_causes,
            "error_summary": e.error_summary,
            "error_id": e.error_id,
            "error_code": e.error_code
        }
        return make_response(jsonify(message), e.status_code)


@bp.route("/<group_id>/users", methods=["GET"])
@authenticated
def get_group_users(group_id):
    """ get users in a group """
    app.logger.debug("get_group_users({0})".format(group_id))
    try:
        response = client.get_group_users(group_id)
        return jsonify(response)
    except OktaError as e:
        message = {
            "error_causes": e.error_causes,
            "error_summary": e.error_summary,
            "error_id": e.error_id,
            "error_code": e.error_code
        }
        return make_response(jsonify(message), e.status_code)


@bp.route("/<group_id>/users/<user_id>", methods=["PUT"])
@authenticated
def add_user_to_group(group_id, user_id):
    """ adds a user to a group """
    app.logger.debug("add_user_to_group({0}, {1})".format(group_id, user_id))
    try:
        response = client.add_user_to_group_by_id(group_id, user_id)
        return jsonify(response)
    except OktaError as e:
        message = {
            "error_causes": e.error_causes,
            "error_summary": e.error_summary,
            "error_id": e.error_id,
            "error_code": e.error_code
        }
        return make_response(jsonify(message), e.status_code)


@bp.route("/<group_id>/users/<user_id>", methods=["DELETE"])
@authenticated
def remove_user_from_group(group_id, user_id):
    """ removes a user from a group """
    app.logger.debug("remove_user_from_group({0}, {1})".format(group_id, user_id))
    try:
        response = client.remove_user_from_group_by_id(group_id, user_id)
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
def get_groups():
    """
    Get a list of groups

    :param limit: maximum number of groups to return
    :type limit: int or None
    :param query: string to search group names
    :type query: str or None
    :rtype: list of UserGroup
    """
    app.logger.debug("get_groups()")
    for item in request.args.items():
        app.logger.debug("argument: {0}".format(item))

    limit = request.args.get("limit") or None
    query = request.args.get("query") or None
    try:
        response = client.get_groups(limit=limit, query=query)
        return jsonify(response)
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
def create_group():
    """ create a group """
    app.logger.debug("create_group()")
    group = request.get_json()
    try:
        response = client.create_group(group)
        return jsonify(response)
    except OktaError as e:
        message = {
            "error_causes": e.error_causes,
            "error_summary": e.error_summary,
            "error_id": e.error_id,
            "error_code": e.error_code
        }
        return make_response(jsonify(message), e.status_code)


@bp.route("/<group_id>", methods=["PUT"])
@authenticated
def update_group(group_id):
    """ update a group """
    app.logger.debug("update_group({0})".format(group_id))
    group = request.get_json()
    try:
        response = client.update_group_by_id(group_id, group)
        return jsonify(response)
    except OktaError as e:
        message = {
            "error_causes": e.error_causes,
            "error_summary": e.error_summary,
            "error_id": e.error_id,
            "error_code": e.error_code
        }
        return make_response(jsonify(message), e.status_code)


@bp.route("/<group_id>", methods=["DELETE"])
@authenticated
def delete_group(group_id):
    """
    Deletes a group
    """
    app.logger.debug("delete_group({0})".format(group_id))
    try:
        response = client.delete_group(group_id)
        return jsonify(response)
    except OktaError as e:
        message = {
            "error_causes": e.error_causes,
            "error_summary": e.error_summary,
            "error_id": e.error_id,
            "error_code": e.error_code
        }
        return make_response(jsonify(message), e.status_code)
