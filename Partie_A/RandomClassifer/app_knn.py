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

# Load Iris dataset from CSV
iris_df = pd.read_csv('iris.csv')  # Update the file path if necessary

# Reduce the size of the dataset
sample_size = 100  # Set the desired size of the sample
iris_df_sample = iris_df.sample(n=sample_size, random_state=42)

# Separate features and target variable
X = iris_df_sample[['sepal.length', 'sepal.width', 'petal.length', 'petal.width']]
y = iris_df_sample['variety']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create KNN classifier
k = 3  # Number of neighbors to consider
knn = KNeighborsClassifier(n_neighbors=k)

# Train the classifier
knn.fit(X_train, y_train)

# Make predictions on the testing set
y_pred = knn.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
classification_rep = classification_report(y_test, y_pred)

# Define a route for model predictions
@app.route('/predict')
def predict():
    # Here, we handle the incoming request and perform predictions using the trained KNN model
    
    # Make predictions on the testing set
    y_pred = knn.predict(X_test)
    
    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    classification_rep = classification_report(y_test, y_pred)
    
    # Prepare response
    response = {
        'accuracy': accuracy,
        'classification_report': classification_rep
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)