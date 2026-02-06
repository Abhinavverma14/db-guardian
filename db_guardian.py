
import psycopg2
import subprocess
import os
import sys

from src.watcher.query_logger import log_query
from src.detector.query_detector import is_dangerous
from src.snapshot.snapshot_manager import create_snapshot
from src.ml.anomaly_detector import is_anomalous

SNAPSHOT_DIR = "snapshots"
DB_NAME = "dbguardian_db"
DB_USER = "postgres"
DB_PASSWORD = "postgres"


def execute_query(query: str):

    # Rule-based dangerous query detection
    if is_dangerous(query):
        print("⚠️ Dangerous query detected!")
        snap = create_snapshot()
        print(f"📸 Snapshot created: {snap}")
        print("❌ Query execution blocked by DB-Guardian")
        return

    # ML anomaly detection
    if is_anomalous(len(query)):
        print("⚠️ ML detected unusual query behavior!")
        snap = create_snapshot()
        print(f"📸 Snapshot created: {snap}")
        print("❌ Query execution blocked (ML anomaly)")
        return

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

        log_query(query)
# Retrain model periodically (simple trigger)
subprocess.run(["python", "src/ml/train_model.py"])


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
        "-c", f"""
        SELECT pg_terminate_backend(pid)
        FROM pg_stat_activity
        WHERE datname = '{DB_NAME}';
        """
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
