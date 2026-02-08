
# DB Guardian


DB-Guardian is a real-time database activity monitoring platform that analyzes SQL queries, detects potentially dangerous operations, and visualizes system activity through a live web dashboard. The system streams query logs via backend APIs, updates dashboard metrics in real time, and provides incident-explanation and recovery-workflow simulation features. Designed with a modular architecture, DB-Guardian can be extended with supervised machine-learning anomaly detection models for enterprise-grade database security monitoring.



## Features

- Real-time SQL query interception
- Rule-based destructive query detection (DELETE/UPDATE without WHERE)
- ML-based anomaly detection for unusual query behavior
- Automatic PostgreSQL snapshot generation using pg_dump
- One-command database restore from snapshots
- Modular architecture (detector, snapshot manager, ML module)
- Automatic ML retraining from query logs


## Architecture

DB-Guardian works as a middleware layer between the application and the database.

Pipeline:
User Query → Query Detector → ML Anomaly Detector → Snapshot Manager → Database

- Safe queries execute normally
- Dangerous queries trigger automatic snapshot creation
- Suspicious queries can be blocked and logged
- Snapshots allow instant point-in-time database recovery


## Tech Stack

- Python

- PostgreSQL

- psycopg2

- pg_dump / psql

- Git & GitHub



## Motivation

Accidental destructive queries such as DELETE without WHERE clauses can cause irreversible data loss in production systems. DB Guardian acts as a protective middleware layer to ensure safe database operations and fast recovery.




## Future Scope

- Supervised SQL anomaly detection models (Logistic Regression / NLP classifiers)
- Cloud snapshot storage (AWS S3)
- Multi-database support (MySQL / MongoDB)
- Real-time production deployment using Docker

