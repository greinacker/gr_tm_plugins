from flask import Flask
from flask_cors import CORS
import os

# Import endpoint modules
from healthcheck import create_blueprint as create_healthcheck_blueprint
from youtube_transcript import create_blueprint as create_youtube_transcript_blueprint
from stockchart import create_blueprint as create_stockchart_blueprint

def create_app():
    """
    Create and configure the Flask application.
    
    Returns:
        Flask: Configured Flask application
    """
    # Get the mount path from environment variable or use default
    mount_path = os.environ.get('MOUNT_PATH', '')
    
    # Create Flask app
    app = Flask(__name__)
    
    # Enable CORS for all domains on all routes
    CORS(app)
    
    # Register blueprints for each endpoint
    app.register_blueprint(create_healthcheck_blueprint(mount_path))
    app.register_blueprint(create_youtube_transcript_blueprint(mount_path))
    app.register_blueprint(create_stockchart_blueprint(mount_path))
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 3001))
    app.run(host='0.0.0.0', port=port)
    