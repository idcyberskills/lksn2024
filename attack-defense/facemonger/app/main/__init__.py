from flask import Flask

from main.config import configure_app

app = Flask(__name__)

app = Flask(__name__, instance_relative_config=True, static_folder='./static', template_folder='./templates')

configure_app(app)

import main.view