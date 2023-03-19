from app import app
import os

if app.config['DEBUG'] == 'False':
    from gevent.pywsgi import WSGIServer
    http_server = WSGIServer((os.getenv('FLASK_RUN_HOST'),int(os.getenv('FLASK_RUN_PORT'))),app)
    http_server.serve_forever()