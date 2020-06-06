#!/bin/zsh
waitress-serve --port=3000 --call 'app:create_app';