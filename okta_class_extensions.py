from okta.models.user.User import User
from okta.models.user.UserProfile import UserProfile


class ExtendedUser(User):
    def __init__(self, **kwargs):
        self.types["profile"] = ExtendedUserProfile
        self.profile = ExtendedUserProfile()
        self.set_profile(**kwargs)


class ExtendedUserProfile(UserProfile):
    types = {
        'windows_username': str,
        'sfdc_id': str
    }

    def __init__(self):
        # merge the types dict from super
        self.types.update(super().types)

        self.windows_username = None
        self.sfdc_id = None
