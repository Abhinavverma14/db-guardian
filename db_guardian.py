import psycopg2
import subprocess
from datetime import datetime
import os
import sys


SNAPSHOT_DIR = "snapshots"
DB_NAME = "dbguardian_db"
DB_USER = "postgres"
DB_PASSWORD = "postgres"


def is_dangerous_query(query: str) -> bool:
    query = query.lower().strip()
    return query.startswith("delete") and "where" not in query


def take_snapshot():
    if not os.path.exists(SNAPSHOT_DIR):
        os.makedirs(SNAPSHOT_DIR)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    snapshot_file = f"{SNAPSHOT_DIR}/snapshot_{timestamp}.sql"

    print(f"📸 Taking snapshot: {snapshot_file}")

    command = ["pg_dump", "-U", DB_USER, DB_NAME]

    with open(snapshot_file, "w") as f:
        subprocess.run(command, stdout=f)

    print("✅ Snapshot created successfully")


def execute_query(query: str):
    if is_dangerous_query(query):
        print("⚠️  Dangerous query detected!")
        take_snapshot()
        print("❌ Query execution blocked by DB-Guardian")
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

    # Terminate active connections
    subprocess.run([
        "psql", "-U", DB_USER, "-d", "postgres",
        "-c", f"""
        SELECT pg_terminate_backend(pid)
        FROM pg_stat_activity
        WHERE datname = '{DB_NAME}';
        """
    ])

    # Drop and recreate database
    subprocess.run(["dropdb", "-U", DB_USER, DB_NAME])
    subprocess.run(["createdb", "-U", DB_USER, DB_NAME])

    # Restore snapshot
    subprocess.run([
        "psql", "-U", DB_USER, "-d", DB_NAME,
        "-f", snapshot_path
    ])

    print("✅ Database restored successfully")


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--restore":
        restore_snapshot(sys.argv[2])
        return

    print("DB-Guardian active with snapshot protection\n")
    query = input("Enter SQL query: ")
    execute_query(query)


if __name__ == "__main__":
    main()
