FROM python:3.9-slim

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY youtube-transcript-server.py .

# Expose the port the app runs on
EXPOSE 3001

# Command to run the application
# Command to run the application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:3001", "youtube-transcript-server:app"]