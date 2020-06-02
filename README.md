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
OKTA_ORG_NAME=https://<ORG_NAME>.okta.com
OKTA_API_TOKEN=
ISSUER=https://<ORG_NAME>.okta.com/oauth2/default
AUDIENCE=api://default
CLIENT_ID=
CLIENT_SECRET=If using PKCE, then this variable is not needed
LOG_LEVEL=DEBUG|INFO|WARNING|ERROR
```

Run the server locally. The default port is 3000.

```shell
python application.py
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
