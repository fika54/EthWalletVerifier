# backend/utils/error_handler.py

from flask import jsonify

def register_error_handlers(app):
    """
    Registers custom error handlers to return JSON instead of HTML.
    """
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Not Found"}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"error": "Server Error"}), 500

    # >>> FILL HERE (Optional)
    # If you want to add more custom errors,
    # e.g., @app.errorhandler(400) etc.

