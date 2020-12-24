import os
from werkzeug.middleware.shared_data import SharedDataMiddleware
from app.application import APP

basedir = os.path.abspath(os.path.dirname(__file__))

def create_app( with_static=True):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.sql')
    app = APP(SQLALCHEMY_DATABASE_URI)
    app.init_database()
    if with_static:
        app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
            '/static':  os.path.join(os.path.dirname(__file__), 'static')
        })
    return app