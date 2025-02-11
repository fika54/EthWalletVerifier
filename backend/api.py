from flask import Flask
from flask_cors import CORS  # Add CORS for handling frontend requests
from routes.ai_chat import ai_chat_bp  # Import the AI Chat Blueprint
from utils.error_handler import register_error_handlers

def create_app():
    """
    Creates the Flask app and registers routes and error handlers.
    """
    app = Flask(__name__)

    # Configurations 
    app.config["DEBUG"] = True

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    app.register_blueprint(ai_chat_bp, url_prefix="/api")  

    register_error_handlers(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5001) 
