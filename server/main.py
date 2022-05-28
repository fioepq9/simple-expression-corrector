from flask import Flask

import dal.db
import handler

if __name__ == "__main__":
    app: Flask = Flask(__name__)
    handler.RegisterRoute(app)
    dal.db.init_db(app)
    app.run(host="0.0.0.0", port=9091, debug=True)
