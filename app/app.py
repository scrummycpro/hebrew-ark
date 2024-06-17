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