import logging
import os
from flask import Flask
from flask_cors import CORS
from okta.framework.Serializer import Serializer

def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.json_encoder = Serializer
    CORS(app)
    app.config.from_object("config.DevConfig")

    with app.app_context():
        logger = logging.getLogger(__name__)
        logging.basicConfig(level=app.config.get("LOG_LEVEL"))
        
        from oktaadminapi import groups, factors, users
        app.register_blueprint(factors.bp, url_prefix="/api/v1/users")
        app.register_blueprint(groups.bp, url_prefix="/api/v1/groups")
        app.register_blueprint(users.bp, url_prefix="/api/v1/users")

        # logger.debug(app.config)
        logger.info("    Org name: {0}".format(app.config.get("ORG_NAME")))
        logger.info("   API token: {0}".format(app.config.get("API_TOKEN")))
        logger.info("      Issuer: {0}".format(app.config.get("ISSUER")))
        logger.info("    Audience: {0}".format(app.config.get("AUDIENCE")))
        logger.info("   Client ID: {0}".format(app.config.get("CLIENT_ID")))
        logger.info("JWKS caching: {0}".format(app.config.get("CACHE_METHOD")))
        logger.info("   S3 Bucket: {0}".format(app.config.get("BUCKET_NAME")))
        return app
