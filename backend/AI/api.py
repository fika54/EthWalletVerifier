from flask import Flask
#from routes.scam_detection import scam_bp
#from routes.wallet_verification import wallet_bp
from routes.ai_chat import ai_chat_bp  # Import the AI Chat Blueprint
from utils.error_handler import register_error_handlers

def create_app():
    """
    Creates the Flask app and registers routes and error handlers.
    """
    app = Flask(__name__)

    # Configurations (optional, can add more)
    app.config["DEBUG"] = True

    # Register Blueprints
  #  app.register_blueprint(scam_bp, url_prefix="/api")
 #   app.register_blueprint(wallet_bp, url_prefix="/api")
    app.register_blueprint(ai_chat_bp, url_prefix="/api")  # Register the AI Chat route

    # Register global error handlers
    register_error_handlers(app)

    return app


if __name__ == '__main__':
    # Run the Flask app
    app = create_app()
    app.run(debug=True)  # You can add `port=5000` to specify a port if needed
