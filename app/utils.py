from os import path
from werkzeug.local import Local, LocalManager
from werkzeug.routing import Map, Rule
from werkzeug import Response
from jinja2 import Environment, FileSystemLoader

local = Local()
local_manager = LocalManager([local])
application = local('application')

TEMPLATE_PATH = path.join(path.dirname(__file__), 'templates')
jinja_env = Environment(loader=FileSystemLoader(TEMPLATE_PATH))


def render_template(template, **context):
    return Response(jinja_env.get_template(template).render(**context),
                    mimetype='text/html')

url_map = Map()
def expose(rule, **kw):
    def decorate(f):
        kw['endpoint'] = f.__name__
        url_map.add(Rule(rule, **kw))
        return f
    return decorate

def url_for(endpoint, _external=False, **values):
    return local.url_adapter.build(endpoint, values, force_external=_external)

jinja_env.globals['url_for'] = url_for