from oktaadminapi import create_app
from okta_class_extensions import ExtendedUser

app = create_app(config_class="config.ProdConfig", user_class=ExtendedUser)
