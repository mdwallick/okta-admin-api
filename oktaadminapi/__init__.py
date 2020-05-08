import os

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "6w_#w*~AVts3!*yd&C]jP0(x_1ssd]MVgzfAw8%fF+c@|ih0s1H&yZQC&-u~O[--"  # For the session
CORS(app)

# sslify = SSLify(app, permanent=True, subdomains=True)

# This must go last to avoid the circular dependency issue
import oktaadminapi.routes