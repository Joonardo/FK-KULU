from flask import Flask

app = Flask(__name__)
app.config.from_object('dev_config')

import .routes
