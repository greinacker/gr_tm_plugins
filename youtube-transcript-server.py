from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import json

# Get the mount path from environment variable or use default
MOUNT_PATH = os.environ.get('MOUNT_PATH', '')

app = Flask(__name__)
# Enable CORS for all domains on all routes
CORS(app)

@app.route(f'{MOUNT_PATH}/youtubetranscript', methods=['POST'])
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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3001))
    app.run(host='0.0.0.0', port=port)