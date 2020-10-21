def classify(features):
    if features['transaction_duration'] <= 1.073:
        return True
    else:
        return False
