from flask import Flask

app = Flask(__name__)
app.config.from_object('dev_config')

if not app.debug:
    import logging
    fh = logging.FileHandler("./log")
    fh.setFormatter(logging.Formatter(app.config["LOG_FORMAT"]))
    fh.setLevel(logging.WARNING)
    app.logger.addHandler(fh)
    logging.getLogger('flask-sqlalchemy').addHandler(fh)

from App import routes
import DB
