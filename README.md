# okta-admin-api
Python server fronting Okta admin APIs using OAuth

## Requirements
* Python >= 3.7
* OktaJWT >= 0.2.6

## Installing
Clone this repo and install the required packages
```
$ git clone https://github.com/mdwallick/okta-admin-api.git
$ cd okta-admin-api
$ pip install -r requirements.txt
```
## Okta Configuration
You need to have an Okta org with API Access management available. You can get a free developer account at https://developer.okta.com. Developer tenants will have API Access Management available.

## Usage
Copy `.env.example` to `.env` and fill out your configuration details.

```
OKTA_ORG_NAME=https://<ORG_NAME>.okta.com
OKTA_API_TOKEN=
ISSUER=https://<ORG_NAME>.okta.com/oauth2/default
AUDIENCE=api://default
CLIENT_ID=
CLIENT_SECRET=If using PKCE, then this variable is not needed
LOG_LEVEL=DEBUG|INFO|WARNING|ERROR
```

Run the server locally. The default port is 3000.
```
python application.py
```
