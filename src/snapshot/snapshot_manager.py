import os
import datetime

def create_snapshot():
    """
    Creates PostgreSQL snapshot using pg_dump
    """

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"snapshots/snapshot_{timestamp}.sql"

    os.system(
        f'pg_dump -U postgres dbguardian_db > {filename}'
    )

    return filename
