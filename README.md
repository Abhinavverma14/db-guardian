\# DB Guardian



DB Guardian is a real-time database safety system that prevents accidental data loss by detecting destructive SQL queries, automatically creating database snapshots, and enabling one-command database restoration.



\## Features

\- Real-time destructive query detection

\- Automatic PostgreSQL snapshot creation using pg\_dump

\- Query execution interception and protection layer

\- One-command database restore from snapshots

\- Timestamped backup storage for point-in-time recovery



\## Tech Stack

\- Python

\- PostgreSQL

\- psycopg2

\- pg\_dump / psql

\- Git \& GitHub



\## Motivation

Accidental destructive queries such as DELETE without WHERE clauses can cause irreversible data loss in production systems. DB Guardian acts as a protective middleware layer to ensure safe database operations and fast recovery.



\## Future Improvements

\- ML-based anomaly detection for unusual query patterns

\- Natural language explanation of detected failures

\- Web dashboard for monitoring

\- Incremental backup strategy using WAL logs



