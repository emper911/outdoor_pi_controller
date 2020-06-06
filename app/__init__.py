import os
import sys
sys.path.append('/Users/riki/Documents/Git/outdoor_pi_controller/app')
from flask import Flask, render_template, send_from_directory
from gardener import get_blueprint

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # INDEX HTML
    @app.route("/", methods=['GET'])
    def root():
        return render_template('index.html')

    app.register_blueprint(get_blueprint())


    return app
