import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import pickle

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

df = pd.read_csv('iris.csv')

X = df.drop('variety', axis=1)
y = df['variety']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression()
model.fit(X_train, y_train)

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)
classification_report_output = classification_report(y_test, predictions)

print(f"Accuracy: {accuracy}")
print("Classification Report:")
print(classification_report_output)

with open('model_setosa.pkl', 'wb') as model_file:
    pickle.dump(model, model_file)

from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/predict', methods=['GET'])
def predict():
    args = request.args
    input_data = [[float(args['sepal.length']), float(args['sepal.width']), float(args['petal.length']), float(args['petal.width'])]]
    
    probabilities = model.predict_proba(input_data).tolist()[0]
    
    class_names = model.classes_
    
    class_probabilities = [{'class': class_name, 'probability': probability} for class_name, probability in zip(class_names, probabilities)]
    
    response = {'class_probabilities': class_probabilities}
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
