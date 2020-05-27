from okta.models.user.User import User
from okta.models.user.UserProfile import UserProfile

"""
If you have custom fields in your Okta user profile
you simply need to extend the User and UserProfile
classes. From there, you need to tell the UsersClient
that you're using a custom User class.

usersClient = UsersClient(
    base_url="https://<YOUR_ORG>.okta.com", 
    api_token="YOUR API TOKEN",
    user_class=ExtendedUser
)
"""


class ExtendedUser(User):
    def __init__(self, **kwargs):
        self.types["profile"] = ExtendedUserProfile
        self.profile = ExtendedUserProfile()
        self.set_profile(**kwargs)


class ExtendedUserProfile(UserProfile):
    types = {
        'goals': str,
        'windows_username': str,
        'sfdc_id': str
    }

    def __init__(self):
        # merge the types dict from super
        self.types.update(super().types)

        self.goals = None
        self.windows_username = None
        self.sfdc_id = None
