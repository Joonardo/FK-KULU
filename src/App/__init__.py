from flask import Flask

app = Flask(__name__)
app.config.from_object('dev_config')

if not app.debug:
    import logging
    fh = logging.FileHandler(app.config["LOG_FILE"])
    fh.setFormatter(logging.Formatter(app.config["LOG_FORMAT"]))
    fh.setLevel(logging.WARNING)
    app.logger.addHandler(fh)
    logging.getLogger('sqlalchemy').addHandler(fh)

from App import routes
import DB
