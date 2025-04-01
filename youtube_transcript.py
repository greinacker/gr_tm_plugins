from flask import Blueprint, request, jsonify
import requests

def create_blueprint(mount_path):
    """
    Create and return a Blueprint for the YouTube transcript endpoint.
    
    Args:
        mount_path (str): The base path where the API is mounted
        
    Returns:
        Blueprint: Flask blueprint with YouTube transcript route
    """
    # Create a blueprint
    youtube_transcript_bp = Blueprint('youtube_transcript', __name__)
    
    @youtube_transcript_bp.route(f'{mount_path}/youtubetranscript', methods=['POST'])
    def youtube_transcript():
        # Check if request contains necessary data
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        
        data = request.get_json()
        
        # Validate input parameters
        if 'api_token' not in data or 'video_id' not in data:
            return jsonify({"error": "Missing required parameters: api_token and video_id"}), 400
        
        api_token = data['api_token']
        video_id = data['video_id']
        
        try:
            # Call the youtube-transcript.io API
            response = requests.post(
                "https://www.youtube-transcript.io/api/transcripts",
                headers={
                    "Authorization": f"Basic {api_token}", 
                    "Content-Type": "application/json"
                },
                json={"ids": [video_id]}
            )
            
            if response.status_code == 200:
                
                # Load the JSON data from the file
                data = response.json()
                
                # Initialize an empty list to store transcript text
                transcript_texts = []
                
                # Navigate to the transcript array and extract the text fields
                for item in data:
                    if 'tracks' in item:
                        for track in item['tracks']:
                            if 'transcript' in track:
                                for entry in track['transcript']:
                                    if 'text' in entry:
                                        transcript_texts.append(entry['text'])
                
                # Concatenate all text fields with spaces
                result = ' '.join(transcript_texts)
                
                # Print the result
                return result, 200
            else:
                # Return the response from the YouTube Transcript API
                return response.json(), response.status_code
            
        except requests.exceptions.RequestException as e:
            return jsonify({"error": f"API request failed: {str(e)}"}), 500
    
    return youtube_transcript_bp
