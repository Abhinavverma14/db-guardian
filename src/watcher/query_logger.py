import os
from datetime import datetime

LOG_FILE = "logs/query_log.csv"

def log_query(query):
    """
    Logs query length and timestamp for ML training
    """

    if not os.path.exists("logs"):
        os.makedirs("logs")

    query_length = len(query)
    timestamp = datetime.now()

    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp},{query_length}\n")
