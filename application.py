import os
from oktaadminapi import create_app

app = create_app(config_class="config.DevConfig")

if __name__ == "__main__":
    # This is to run on c9.io or locally; you may need to change or make your own runner
    app.run(host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 8000)), debug=True)
