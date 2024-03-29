import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import r2_score
from flask import Flask, request, jsonify

app = Flask(__name__)

data = pd.read_csv('Housing.csv', delimiter= ',')
df = pd.DataFrame(data).dropna()

binary_mappings = {'yes': 1, 'no': 0}
df[['mainroad', 'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 'prefarea']] = \
    df[['mainroad', 'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 'prefarea']].applymap(lambda x: binary_mappings.get(x, x))
df['furnishingstatus'] = df['furnishingstatus'].map({'furnished': 1, 'semi-furnished': 0})

df.fillna(df.mean(), inplace=True)

X = df.drop('price', axis=1)
y = df['price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

dt_model = DecisionTreeRegressor()
dt_model.fit(X_train, y_train)

@app.route('/predict', methods=['GET'])
def predict():
    try:
        input_params = {key: float(request.args.get(key)) for key in X.columns}

        prediction = dt_model.predict(pd.DataFrame([input_params]))[0]

        response = {'prediction': prediction}
        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
