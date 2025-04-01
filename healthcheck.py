from flask import Blueprint

def create_blueprint(mount_path):
    """
    Create and return a Blueprint for the healthcheck endpoint.
    
    Args:
        mount_path (str): The base path where the API is mounted
        
    Returns:
        Blueprint: Flask blueprint with healthcheck route
    """
    # Create a blueprint
    healthcheck_bp = Blueprint('healthcheck', __name__)
    
    @healthcheck_bp.route(f'{mount_path}/healthcheck', methods=['GET'])
    def healthcheck():
        """Simple health check endpoint that returns HTTP 200"""
        return "", 200
    
    return healthcheck_bp
