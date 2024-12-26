from flask import Flask
from user_routes import user_routes
from middleware import (
    error_logging_middleware,
    simple_validation_middleware,
    cors_middleware,
)

app = Flask(__name__)

app.register_blueprint(user_routes)

cors_middleware(app)

error_logging_middleware(app)

simple_validation_middleware(app)

if __name__ == "__main__":
    app.run(debug=True)
