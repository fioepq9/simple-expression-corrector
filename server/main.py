from flask import Flask
from flask_jwt_extended import JWTManager

import config
import dal.db as db
import handler
import model

if __name__ == "__main__":
    app: Flask = Flask(__name__)

    model.init_model()
    handler.init_app(app)
    db.init_app(app)

    app.config['JWT_SECRET_KEY'] = config.APP_name
    app.config['JWT_TOKEN_LOCATION'] = ['headers', 'json']
    app.config['JWT_JSON_KEY'] = 'token'
    jwt = JWTManager(app)

    app.run(host="0.0.0.0", port=9091, debug=True)
