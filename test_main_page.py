from app import create_app
from webtest import TestApp
app = TestApp(create_app())

def test_main():
    resp = app.get('/')
    assert resp.status == '200 OK'
