import logging
import os

from flask import Flask
from flask_cors import CORS

from okta.UsersClient import UsersClient
from okta.framework.Serializer import Serializer
from okta.models.user.User import User


def create_app(config_class="config.ProdConfig", user_class=User):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.json_encoder = Serializer
    CORS(app)
    app.config.from_object(config_class)

    with app.app_context():
        logger = logging.getLogger(__name__)
        log_level = app.config.get("LOG_LEVEL")
        logging.basicConfig(level=log_level)

        from oktaadminapi import groups, factors, users
        app.register_blueprint(factors.bp, url_prefix="/api/v1/users")
        app.register_blueprint(groups.bp, url_prefix="/api/v1/groups")
        app.register_blueprint(users.bp, url_prefix="/api/v1/users")

        # set up the users client. we have to do this here because there's
        # no other way to get the custom User subclass into the blueprint
        app.usersClient = UsersClient(base_url=app.config.get("ORG_NAME"),
                                      api_token=app.config.get("API_TOKEN"),
                                      user_class=user_class)

        logger.info("Org name: {0}".format(app.config.get("ORG_NAME")))
        logger.info("API token: {0}".format(app.config.get("API_TOKEN")))
        logger.info("Issuer: {0}".format(app.config.get("ISSUER")))
        logger.info("Audience: {0}".format(app.config.get("AUDIENCE")))
        logger.info("JWKS caching: {0}".format(app.config.get("CACHE_METHOD")))
        logger.info("S3 Bucket: {0}".format(app.config.get("BUCKET_NAME")))
        return app
