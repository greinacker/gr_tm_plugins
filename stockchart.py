from flask import Blueprint, request, jsonify
import requests

def create_blueprint(mount_path):
    """
    Create and return a Blueprint for the Stock Chart endpoint.
    
    Args:
        mount_path (str): The base path where the API is mounted
        
    Returns:
        Blueprint: Flask blueprint with Stock Chart route
    """
    # Create a blueprint
    stockchart_bp = Blueprint('stockchart', __name__)
    
    @stockchart_bp.route(f'{mount_path}/stockchart', methods=['POST'])
    def stockchart():
        """
        Endpoint to fetch stock chart data.
        """
        # Check if request contains necessary data
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400

        data = request.get_json()

        # Validate input parameters
        if 'api_token' not in data or 'symbol' not in data:
            return jsonify({"error": "Missing required parameters: api_token and symbol"}), 400

        api_token = data['api_token']
        symbol = data['symbol']

        try:
            # Call a hypothetical stock chart API
            response = requests.post(
                f"https://api.chart-img.com/v2/tradingview/advanced-chart/storage",
                headers={
                    "x-api-key": f"{api_token}",
                    "Content-Type": "application/json"
                },
                json={"symbol": f"{symbol}", 
                      "studies": [ 
                          { "name": "Volume", "forceOverlay": "true" },
                          {"name": "Moving Average",
                            "input": {
                                "length": 200,
                                "smoothingLength": 200
                            },
                            "override": {
                                "Plot.color": "rgb(64,192,255)"
                            }
                          },
                          {"name": "Moving Average",
                            "input": {
                                "length": 50,
                                "smoothingLength": 50
                            },
                            "override": {
                                "Plot.color": "rgb(255,64,64)"
                            }
                          }
                            ]}
            )

            if response.status_code == 200:
                # Return the stock chart data
                return response.json(), 200
            else:
                # Return the response from the stock chart API
                return response.json(), response.status_code

        except requests.exceptions.RequestException as e:
            return jsonify({"error": f"API request failed: {str(e)}"}), 500

    return stockchart_bp
