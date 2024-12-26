from flask import jsonify, request
import logging
import traceback

# simple logging configuration
# in future can be integrated into tools like Sentry to better interface with logs
logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs/errors.log"), logging.StreamHandler()],
)


# cors middleware to prevent CORS attack
# currently "*" routes are allowed, in production specific routes will be allowed to cross
def cors_middleware(app):
    @app.after_request
    def add_cors_headers(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = (
            "GET, POST, PUT, DELETE, OPTIONS"
        )
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"

        if request.method == "OPTIONS":
            response.status_code = 204

        return response


# error logging middleware, better formatted errors
def error_logging_middleware(app):
    @app.errorhandler(Exception)
    def handle_exception(e):
        logging.error(
            f"Exception occurred: {str(e)}\n"
            f"Path: {request.path}\n"
            f"Method: {request.method}\n"
            f"Headers: {dict(request.headers)}\n"
            f"Body: {request.data.decode('utf-8')}\n"
            f"Traceback: {traceback.format_exc()}"
        )

        return jsonify({"error": "error occured!"}), 500


# validation middleware, check the request body has content of type json
def simple_validation_middleware(app):
    @app.before_request
    def validate_content_type():
        if request.method in ["POST", "PUT", "PATCH"]:
            if request.content_type != "application/json":
                return jsonify({"error": "invalid content type!"}), 415
