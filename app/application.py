from os import path
from sqlalchemy import create_engine, MetaData
from werkzeug import Request
from werkzeug.wsgi import ClosingIterator
from werkzeug.exceptions import HTTPException, NotFound
from app.utils import local, local_manager, url_map, render_response
from app import views, models

class APP(object):

    def __init__(self, db_uri):
        local.application = self
        self.database_engine = create_engine(db_uri)

    def init_database(self):
        models.Base.metadata.create_all(self.database_engine)
    
    def wsgi_app(self, environ, start_response):
        local.application = self
        request = Request(environ)
        response = self.dispatch_request(environ, request)
        return response(environ, start_response)
    
    def error_404(self):
        response = render_response({"Message":"Error 404, Page not found try checking the url"})
        response.status_code = 404
        return response

    def dispatch_request(self, environ, request):
        
        local.url_adapter = adapter = url_map.bind_to_environ(environ)
        try:
            endpoint, values = adapter.match()
            handler = getattr(views, endpoint)
            return handler(request, **values)
        except NotFound:
            return self.error_404()
        except HTTPException as e:
            return e

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)