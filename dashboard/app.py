from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__)

LOG_FILE = "../logs/query_log.json"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/logs")
def get_logs():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE) as f:
            data = json.load(f)
    else:
        data = []

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
