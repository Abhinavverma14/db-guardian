import threading
import time
import random

from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__)

LOG_FILE = "query_log.json"

# ---------- Create sample logs if not exist ----------
if not os.path.exists(LOG_FILE):
    sample_logs = [
        {"time": "10:30", "query": "DROP TABLE users", "status": "Blocked"},
        {"time": "10:32", "query": "SELECT * FROM accounts", "status": "Safe"},
        {"time": "10:35", "query": "DELETE FROM payments", "status": "Blocked"}
    ]
    with open(LOG_FILE, "w") as f:
        json.dump(sample_logs, f)


def generate_demo_logs():
    queries = [
        ("SELECT * FROM users", "Safe"),
        ("UPDATE accounts SET balance=100", "Safe"),
        ("DELETE FROM users", "Blocked"),
        ("DROP TABLE payments", "Blocked"),
        ("INSERT INTO orders VALUES(...)", "Safe"),
    ]

    while True:
        time.sleep(10)

        if os.path.exists(LOG_FILE):
            with open(LOG_FILE) as f:
                data = json.load(f)
        else:
            data = []

        q, status = random.choice(queries)

        data.append({
            "time": time.strftime("%H:%M:%S"),
            "query": q,
            "status": status
        })

        with open(LOG_FILE, "w") as f:
            json.dump(data, f)


# start background simulator
threading.Thread(target=generate_demo_logs, daemon=True).start()


@app.route("/")
def home():
    return render_template("index.html")


# ---------- Logs API ----------
@app.route("/api/logs")
def get_logs():
    with open(LOG_FILE) as f:
        data = json.load(f)
    return jsonify(data)


# ---------- Stats API ----------
@app.route("/api/stats")
def get_stats():
    with open(LOG_FILE) as f:
        data = json.load(f)

    total = len(data)
    blocked = sum(1 for x in data if x["status"] == "Blocked")
    snapshots = 3  # demo value

    return jsonify({
        "total": total,
        "blocked": blocked,
        "snapshots": snapshots
    })


if __name__ == "__main__":
    app.run(debug=True)
