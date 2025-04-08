from flask import Flask
from flask_cors import CORS
import sys
import os

# Add parent directory to path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from youtube_transcript import create_blueprint as create_youtube_transcript_blueprint
from stockchart import create_blueprint as create_stockchart_blueprint
from healthcheck import create_blueprint as create_healthcheck_blueprint

app = Flask(__name__)
CORS(app)

# Register blueprints with empty mount path for Vercel
app.register_blueprint(create_healthcheck_blueprint(''))
app.register_blueprint(create_youtube_transcript_blueprint(''))
app.register_blueprint(create_stockchart_blueprint(''))

