import logging
import os

from flask import abort, jsonify, make_response, request
from flask import current_app as app
from functools import wraps

from oktajwt import (
    JwtVerifier,
    ExpiredTokenError,
    InvalidSignatureError,
    KeyNotFoundError,
    InvalidKeyError
)


@app.errorhandler(401)
def not_authorized(error):
    message = {
        "error": "Unauthorized",
        "message": "Invalid, expired or missing bearer token"
    }
    return make_response(jsonify(message), 401)


@app.errorhandler(404)
def not_found(error):
    message = {
        "error": "Not found"
    }
    return make_response(jsonify(message), 404)


def authenticated(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        app.logger.debug("authenticated()")

        # Just validate they have a legit token.
        # Any additional access rules will be by another wrapper
        access_token = get_access_token()
        if is_operation_allowed(access_token):
            return f(*args, **kws)
        else:
            abort(401)

    return decorated_function


def get_access_token():
    access_token = None
    authorization_header = request.headers.get("authorization")
    app.logger.debug("Authorization header {0}".format(authorization_header))

    if authorization_header == None:
        abort(401)
    else:
        header = "Bearer"
        bearer, access_token = authorization_header.split(" ")
        if bearer != header:
            abort(401)

    return access_token


def is_operation_allowed(token):
    """
    Given the information in token, is this transaction authorized.
    """
    app.logger.debug("is_operation_allowed()")
    issuer = app.config.get("ISSUER")
    audience = app.config.get("AUDIENCE")
    cache_method = app.config.get("CACHE_METHOD")
    bucket_name = app.config.get("BUCKET_NAME")

    try:
        jwtVerifier = JwtVerifier(issuer, audience, cache_method=cache_method, bucket_name=bucket_name)
        claims = jwtVerifier.verify(token)
        # should we check extra scopes or anything like that?
        return claims["iss"] == issuer and claims["aud"] == audience
    except Exception as e:
        app.logger.error(e)
        return False
