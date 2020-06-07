#!/bin/zsh
#export PYTHON_PATH=$PYTHON_PATH:/home/pi/Documents/Git/outdoor_pi_controller/app;
waitress-serve --port=3000 --host=0.0.0.0 --call 'app:create_app';
