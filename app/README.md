# Flask Hebrew Studies Application

This guide details the steps to create and run a Flask application that fetches Hebrew studies data and serves it via a web interface, containerized using Docker with an Alpine base image.

## Prerequisites

Ensure you have the following installed:
- Docker
- Python (for local testing)

## Application Setup

### 1. Flask Application Code

Create a file named `app.py` with the following content:

```python
from flask import Flask, jsonify, render_template_string
import sqlite3
import subprocess
import json
from datetime import datetime

app = Flask(__name__)

def save_to_database(timestamp, hebrew_topic, calendar_data):
    try:
        conn = sqlite3.connect('hebrew_studies.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS commands (
                            id INTEGER PRIMARY KEY,
                            timestamp TEXT,
                            hebrew_topic TEXT,
                            calendar_data TEXT
                        )''')
        cursor.execute("INSERT INTO commands (timestamp, hebrew_topic, calendar_data) VALUES (?, ?, ?)",
                       (timestamp, hebrew_topic, calendar_data))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"An error occurred: {e}")

def fetch_data():
    hebrew_command = "curl --silent --request GET --url https://www.sefaria.org/api/texts/random-by-topic --header 'accept: application/json'"
    calendar_command = "curl --silent --request GET --url https://www.sefaria.org/api/calendars --header 'accept: application/json'"

    hebrew_output, _ = subprocess.Popen(hebrew_command.split(), stdout=subprocess.PIPE, text=True).communicate()
    calendar_output, _ = subprocess.Popen(calendar_command.split(), stdout=subprocess.PIPE, text=True).communicate()

    hebrew_json_result = json.loads(hebrew_output)
    calendar_json_result = json.loads(calendar_output)

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    hebrew_topic = hebrew_json_result.get('topic', {}).get('primaryTitle', {}).get('he', 'Unknown')
    calendar_data = json.dumps(calendar_json_result, ensure_ascii=False, indent=4)

    save_to_database(timestamp, hebrew_topic, calendar_data)

    return hebrew_json_result, calendar_json_result

@app.route('/')
def index():
    hebrew_data, calendar_data = fetch_data()
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hebrew Studies</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/bootswatch/5.1.3/darkly/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background-color: #121212;
            color: #e0e0e0;
        }
        .container {
            margin-top: 20px;
        }
        .card {
            background-color: #1e1e1e;
            color: #e0e0e0;
            margin-bottom: 20px;
        }
        .card-body {
            white-space: pre-wrap;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="text-center">Study This Today</h1>
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">Hebrew Topic Data</h5>
                <p><strong>Reference:</strong> {{ hebrew_data['ref'] }}</p>
                <p><strong>Topic:</strong> {{ hebrew_data['topic']['primaryTitle']['he'] }} ({{ hebrew_data['topic']['primaryTitle']['en'] }})</p>
                <p><strong>URL:</strong> <a href="https://www.sefaria.org/{{ hebrew_data['url'] }}">{{ hebrew_data['url'] }}</a></p>
            </div>
        </div>
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">Calendar Data</h5>
                <p><strong>Date:</strong> {{ calendar_data['date'] }}</p>
                <p><strong>Timezone:</strong> {{ calendar_data['timezone'] }}</p>
                <div>
                    <h6>Items:</h6>
                    <ul>
                        {% for item in calendar_data['calendar_items'] %}
                        <li>
                            <strong>{{ item['title']['he'] }} ({{ item['title']['en'] }})</strong>
                            <ul>
                                <li><strong>Display Value:</strong> {{ item['displayValue']['he'] }} ({{ item['displayValue']['en'] }})</li>
                                <li><strong>Reference:</strong> {{ item['heRef'] }} ({{ item['ref'] }})</li>
                                <li><strong>Description:</strong> {{ item.get('description', {}).get('he', '') }}</li>
                                <li><strong>URL:</strong> <a href="https://www.sefaria.org/{{ item['url'] }}">{{ item['url'] }}</a></li>
                            </ul>
                        </li>
                        {% endfor %}
                    </ul>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
''', hebrew_data=hebrew_data, calendar_data=calendar_data)

@app.route('/api/data')
def api_data():
    hebrew_data, calendar_data = fetch_data()
    return jsonify({"hebrew_data": hebrew_data, "calendar_data": calendar_data})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
```

### 2. Create Dockerfile

Create a file named `Dockerfile` with the following content:

```Dockerfile
# Use the official Python 3.9 Alpine image from the Docker Hub
FROM python:3.9-alpine

# Set the working directory in the container
WORKDIR /app

# Install required dependencies
RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev curl

# Copy the current directory contents into the container at /app
COPY . /app

# Install Flask and Werkzeug with compatible versions
RUN pip install flask==2.1.1 werkzeug==2.0.3

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "app.py"]
```

### 3. Build the Docker Image

Build the Docker image using the following command:

```sh
docker build -t flask-hebrew-studies .
```

### 4. Run the Docker Container

Run the Docker container with the following command:

```sh
docker run -p 4000:80 flask-hebrew-studies
```

### 5. Access the Application

Open your web browser and navigate to `http://localhost:4000/` to see your Flask application running inside the Docker container.

## Summary

1. **Flask Application**: Created a Flask app that fetches data from the Sefaria API and displays it on a web page.
2. **Dockerfile**: Used the Alpine-based Python image to create a lightweight container.
3. **Dependencies**: Installed necessary dependencies including Flask and Werkzeug.
4. **Build and Run**: Built the Docker image and ran the container, mapping port 4000 on the host to port 80 in the container.

This approach ensures a lightweight, reproducible environment for running the Flask application.