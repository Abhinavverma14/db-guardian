import psycopg2
import subprocess
from datetime import datetime
import os
import sys

from src.detector.query_detector import is_dangerous
from src.snapshot.snapshot_manager import create_snapshot
from src.ml.anomaly_detector import is_anomalous
from src.ml.explanation_generator import generate_explanation

SNAPSHOT_DIR = "snapshots"
DB_NAME = "dbguardian_db"
DB_USER = "postgres"
DB_PASSWORD = "postgres"


def execute_query(query: str):

    # Rule-based dangerous detection
    if is_dangerous(query):
        print("⚠️ Dangerous query detected!")

        snap = create_snapshot()

        explanation = generate_explanation(
            "A destructive SQL operation such as DELETE without WHERE clause was detected."
        )

        print(f"📸 Snapshot created: {snap}")
        print("\nExplanation:")
        print(explanation)

        print("❌ Query execution blocked by DB-Guardian")
        return

    # ML anomaly detection
    if is_anomalous(len(query)):
        print("⚠️ ML detected unusual query behavior!")

        snap = create_snapshot()

        explanation = generate_explanation(
            "An unusual SQL query pattern was detected by the anomaly detection model."
        )

        print(f"📸 Snapshot created: {snap}")
        print("\nExplanation:")
        print(explanation)

        print("❌ Query execution blocked (ML anomaly)")
        return

    # Normal execution
    try:
        conn = psycopg2.connect(
            host="localhost",
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )

        cur = conn.cursor()
        cur.execute(query)
        conn.commit()

        cur.close()
        conn.close()

        print("✅ Query executed successfully")

    except Exception as e:
        print("Execution failed:", e)


def restore_snapshot(snapshot_name: str):

    snapshot_path = os.path.join(SNAPSHOT_DIR, snapshot_name)

    if not os.path.exists(snapshot_path):
        print("❌ Snapshot not found")
        return

    print(f"♻️ Restoring snapshot: {snapshot_name}")

    subprocess.run([
        "psql", "-U", DB_USER, "-d", "postgres",
        "-c",
        f"SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '{DB_NAME}';"
    ])

    subprocess.run(["dropdb", "-U", DB_USER, DB_NAME])
    subprocess.run(["createdb", "-U", DB_USER, DB_NAME])

    subprocess.run([
        "psql", "-U", DB_USER, "-d", DB_NAME,
        "-f", snapshot_path
    ])

    print("✅ Database restored successfully")


def main():

    if len(sys.argv) == 3 and sys.argv[1] == "--restore":
        restore_snapshot(sys.argv[2])
        return

    print("DB-Guardian active (AI + modular protection)\n")

    query = input("Enter SQL query: ")
    execute_query(query)


if __name__ == "__main__":
    main()
