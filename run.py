from waitress import serve
from MyDjango.wsgi import application
import os
import venv
venv.main
serve(
    app=application,
    host='127.0.0.1',
    port=8080
)
