from flask import Flask

app = Flask(__name__)
app.config.from_object('dev_config')

if not app.debug:
    import logging
    fh = logging.FileHandler(app.config["LOG_FILE"])
    fh.setLevel(logging.WARNING)
    app.logger.addHandler(fh)

from App import routes
import DB
