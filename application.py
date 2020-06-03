import os
from oktaadminapi import create_app
from okta_class_extensions import ExtendedUser

if __name__ == "__main__":
    # This is to run on c9.io or locally; you may need to change or make your own runner
    app = create_app(config_class="config.DevConfig", user_class=ExtendedUser)
    app.run(host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 8000)), debug=True)
