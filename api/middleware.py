from flask import jsonify, request
import logging
import traceback

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("error.log"), logging.StreamHandler()],
)


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

        return jsonify(
            {"error": "An unexpected error occurred. Please try again later."}
        ), 500


def simple_validation_middleware(app):
    @app.before_request
    def validate_content_type():
        if request.method in ["POST", "PUT", "PATCH"]:
            if request.content_type != "application/json":
                return jsonify(
                    {
                        "error": "Invalid Content-Type. Only 'application/json' is supported."
                    }
                ), 415
