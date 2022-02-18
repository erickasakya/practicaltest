from werkzeug.serving import run_simple
from app import create_app

if __name__ == '__main__':
    app = create_app()
    run_simple('0.0.0.0', 5000, app, use_debugger=True, use_reloader=True)
