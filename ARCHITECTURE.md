\# DB-Guardian Architecture



User Query

&nbsp;  ↓

DB-Guardian Middleware

&nbsp;  ↓

Query Detector

&nbsp;  ├── Rule-based detection

&nbsp;  └── ML anomaly detection

&nbsp;  ↓

If Dangerous:

&nbsp;  ├── Snapshot created (pg\_dump)

&nbsp;  ├── Query blocked

&nbsp;  └── Logged for training

Else:

&nbsp;  └── Query executed

&nbsp;  ↓

Query Logger → Training Dataset → ML Retraining



