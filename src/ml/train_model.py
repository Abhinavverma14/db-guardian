import pandas as pd
import joblib
from sklearn.ensemble import IsolationForest

LOG_FILE = "logs/query_log.csv"
MODEL_FILE = "src/ml/anomaly_model.pkl"

def train_model():
    try:
        data = pd.read_csv(LOG_FILE, header=None)
        data.columns = ["timestamp", "query_length"]

        X = data[["query_length"]]

        model = IsolationForest(contamination=0.05)
        model.fit(X)

        joblib.dump(model, MODEL_FILE)

        print("Model trained and saved successfully")

    except Exception as e:
        print("Training failed:", e)


if __name__ == "__main__":
    train_model()
