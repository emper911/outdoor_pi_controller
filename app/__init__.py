import os
import sys
sys.path.append('/home/pi/Documents/Git/outdoor_pi_controller/app')
from flask import Flask, render_template, send_from_directory
from app import gardener


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

    app.register_blueprint(gardener.get_blueprint())
    
    return app

def exit_gracefully():
    gardener.cleanup_gpios()
    print('Server is terminating\n\nBye Bye Now :)')
    sys.exit(0)
