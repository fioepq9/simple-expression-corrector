from flask import Flask
import handler


if __name__ == "__main__":
    app: Flask = Flask(__name__)
    handler.init_app(app)
    app.run(host="0.0.0.0", port=8080, debug=True)
