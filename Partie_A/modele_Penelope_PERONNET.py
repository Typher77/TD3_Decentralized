# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 18:07:46 2024

@author: Admin
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report
import numpy as np

iris_df = pd.read_csv('iris.csv')  

sample_size = 25 
iris_df_sample = iris_df.sample(n=sample_size, random_state=42)

X = iris_df_sample[['sepal.length', 'sepal.width', 'petal.length', 'petal.width']]
y = iris_df_sample['variety']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)

k = 3  # Number of neighbors to consider
knn = KNeighborsClassifier(n_neighbors=k)

knn.fit(X_train, y_train)

y_pred = knn.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

print("Classification Report:")
print(classification_report(y_test, y_pred))
