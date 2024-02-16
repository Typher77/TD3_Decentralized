# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 19:11:04 2024

@author: Admin
"""
from flask import Flask, jsonify
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report
import numpy as np

app = Flask(__name__)

iris_df = pd.read_csv('iris.csv')  # Update the file path if necessary

sample_size = 100  # Set the desired size of the sample
iris_df_sample = iris_df.sample(n=sample_size, random_state=42)

X = iris_df_sample[['sepal.length', 'sepal.width', 'petal.length', 'petal.width']]
y = iris_df_sample['variety']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

k = 3  # Number of neighbors to consider
knn = KNeighborsClassifier(n_neighbors=k)

knn.fit(X_train, y_train)

y_pred = knn.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
classification_rep = classification_report(y_test, y_pred)

@app.route('/predict')
def predict():
    
    y_pred = knn.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    classification_rep = classification_report(y_test, y_pred)
    
    response = {
        'accuracy': accuracy,
        'classification_report': classification_rep
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
