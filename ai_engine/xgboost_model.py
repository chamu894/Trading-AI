import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
import joblib

def create_features(df):

    df = df.copy()

    # Price movement
    df['body'] = df['close'] - df['open']

    # Volatility
    df['range'] = df['high'] - df['low']

    # Direction
    df['direction'] = (df['close'] > df['open']).astype(int)

    # Momentum
    df['momentum'] = df['close'] - df['close'].shift(1)

    df = df.dropna()

    return df

def create_labels(df, forward=5):

    df = df.copy()

    df['future_price'] = df['close'].shift(-forward)

    df['target'] = (df['future_price'] > df['close']).astype(int)

    df = df.dropna()

    return df


def train_model(df):

    features = ['body', 'range', 'direction', 'momentum']

    X = df[features]
    y = df['target']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        shuffle=False
    )

    model = XGBClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1
    )

    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test)

    print("MODEL ACCURACY:", accuracy)

    return model

def save_model(model, path="ai_engine/model.pkl"):
    joblib.dump(model, path)

def predict(model, latest_row):

    features = ['body', 'range', 'direction', 'momentum']

    X = latest_row[features].values.reshape(1, -1)

    prob = model.predict_proba(X)[0][1]

    return prob