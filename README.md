# okta-admin-api

Python server fronting Okta admin APIs using OAuth. This is useful for
cases where you need to do admin stuff in an app, but you don't want to
or can't have an Okta API token in the app (e.g. SPA or native mobile app).

## Requirements

* Python >= 3.7
* OktaJWT >= 0.3.4
* okta-sdk-python >= 0.2.0

## Installing

Clone this repo and install the required packages

```shell
git clone https://github.com/mdwallick/okta-admin-api.git
cd okta-admin-api
pip install -r requirements.txt
```

## Okta Configuration

You need to have an Okta org with API Access management available. You can
get a free developer account at [developer.okta.com](https://developer.okta.com).
Developer tenants will have API Access Management available.

## Usage

Copy `.env.example` to `.env` and fill out your configuration details.

```shell
ORG_NAME=https://<ORG_NAME>.okta.com
API_TOKEN=
ISSUER=https://<ORG_NAME>.okta.com/oauth2/default
AUDIENCE=api://default
LOG_LEVEL=DEBUG|INFO|WARNING|ERROR
```

Run the server locally. The default port is 8000.

```shell
python application.py
```

If you have extended the Okta user profile and wish to see/use those new fields,
you need to subclass the base User and UserProfile classes and pass your new
user class name into the call to `create_app`.

For running locally:

```python
# application.py
import os
from oktaadminapi import create_app

# import your User subclass
from okta_class_extensions import ExtendedUser

if __name__ == "__main__":
    # config_class defaults to "config.ProdConfig" if not specified
    # user_class defaults to "User" if not specified
    app = create_app(config_class="config.DevConfig", user_class=ExtendedUser)
    app.run(host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 8000)), debug=True)
```

Using wsgi.py (AWS Elastic Beanstalk, e.g.)

```python
# wsgi.py
from oktaadminapi import create_app
from okta_class_extensions import ExtendedUser

app = create_app(user_class=ExtendedUser)
```

Example subclasses are in `okta_class_extensions.py`.

```python
# okta_class_extensions.py
from okta.models.user.User import User
from okta.models.user.UserProfile import UserProfile

class ExtendedUser(User):
    def __init__(self, **kwargs):
        self.types["profile"] = ExtendedUserProfile
        self.profile = ExtendedUserProfile()
        self.set_profile(**kwargs)


class ExtendedUserProfile(UserProfile):
    # My Okta user profile has two extra fields
    types = {
        'windows_username': str,
        'sfdc_id': str
    }

    def __init__(self):
        # merge the types dict from super
        self.types.update(super().types)

        self.windows_username = None
        self.sfdc_id = None
```

## APIs Implemented

### Users - [API docs](https://developer.okta.com/docs/reference/api/users/)

[User Operations](https://developer.okta.com/docs/reference/api/users/#user-operations)

* Create
* Get User
* List Users
* Update User

[Related Resources](https://developer.okta.com/docs/reference/api/users/#related-resources)

* Get Assigned App Links
* Get User's Groups

[Lifecycle Operations](https://developer.okta.com/docs/reference/api/users/#lifecycle-operations)

* Activate
* Reactivate
* Deactivate
* Suspend
* Unsuspend
* Delete
* Unlock
* Reset Password
* Expire Password
* Reset Factors
* ~~Clear Current User Sessions~~

[Credential Operations](https://developer.okta.com/docs/reference/api/users/#credential-operations)

* ~~Forgot Password~~
* Change Password
* ~~Change Recovery Question~~

### [Factors](https://developer.okta.com/docs/reference/api/factors/)

[Factor Operations](https://developer.okta.com/docs/reference/api/factors/#factor-operations)

* Get Factor
* List enrolled factors
* List factors to enroll
* List security questions

[Factor Lifecycle Operations](https://developer.okta.com/docs/reference/api/factors/#factor-lifecycle-operations)

* Enroll

  * Security Question
  * SMS
  * Call
  * Okta Verify OTP
  * Okta Verify Push
  * Google Authenticator
  * ~~RSA SecurID~~
  * ~~Symantec VIP~~
  * ~~Yubikey~~
  * Email
  * ~~U2F~~
  * ~~WebAuthN~~
  * ~~Custom HOTP~~

* Activate

  * TOTP
  * SMS
  * Call
  * Push
  * Email
  * ~~U2F~~
  * ~~WebAuthN~~

* Reset

Challenge/Verify

* SMS
* Call
* Push
* Email
* ~~U2F~~
* ~~WebAuthN~~
* Security Question
* TOTP
* ~~Token~~
* ~~Yubikey~~

### [Groups](https://developer.okta.com/docs/reference/api/groups/)

[Group Operations](https://developer.okta.com/docs/reference/api/groups/#group-operations)

* Add Group
* Get Group
* List Groups
* Update Group
* Remove Group

[Group Member Operations](https://developer.okta.com/docs/reference/api/groups/#group-member-operations)

* List Group Members
* Add User to Group
* Remove User from Group
