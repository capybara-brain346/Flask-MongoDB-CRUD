from flask import jsonify, request
import logging
import traceback

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs/errors.log"), logging.StreamHandler()],
)


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


def simple_validation_middleware(app):
    @app.before_request
    def validate_content_type():
        if request.method in ["POST", "PUT", "PATCH"]:
            if request.content_type != "application/json":
                return jsonify({"error": "invalid content type!"}), 415
