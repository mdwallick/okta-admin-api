import logging
import os

from oktaadminapi import app as application

logger = logging.getLogger(__name__)
loglevel = os.getenv("LOG_LEVEL", "WARNING")
logging.basicConfig(level=loglevel)

if __name__ == "__main__":
    # This is to run on c9.io or locally; you may need to change or make your own runner
    application.run(host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 3000)), debug=True)