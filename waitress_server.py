import signal
import sys
from waitress import serve
from app import create_app


def signal_handler(sig, frame):
    print('Server is terminating! Cleaning up GPIO PINS on exit!')
    # GPIO.cleanup()
    sys.exit(0)

# Exit gracefully
signal.signal(signal.SIGINT, signal_handler)
signal.pause()

#####################################################################
###########################  ENTRY POINT  ###########################
#####################################################################
app = create_app()
serve(app, port=3000)
# serve(app, listen='*:8080')

