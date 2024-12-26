# wsgi server to replace the built-in flask server to make it production level
from app import app

if __name__ == "__main__":
    app.run()
