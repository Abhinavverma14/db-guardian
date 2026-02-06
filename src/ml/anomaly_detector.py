from sklearn.ensemble import IsolationForest
import numpy as np

# Dummy training data (query sizes)
data = np.array([
    [20], [25], [30], [35], [40], [50], [60], [80], [100]
])

model = IsolationForest(contamination=0.1)
model.fit(data)


def is_anomalous(query_length):
    """
    Detect abnormal query size
    """
    pred = model.predict([[query_length]])
    return pred[0] == -1
