import signal
import sys
from waitress import serve
import waitress
from app import create_app, exit_gracefully
#####################################################################
###########################  ENTRY POINT  ###########################
#####################################################################
def main(app):
    serve(app, host="0.0.0.0", port=80)
    # serve(app, listen='*:8080')

if __name__ == '__main__':
    app = create_app()
    try:
        main(app)
    except KeyboardInterrupt:
        pass
    finally:
        exit_gracefully()
