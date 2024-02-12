# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 19:53:59 2024

@author: Admin
"""

from flask import Flask, request, jsonify
from requests import get

app = Flask(__name__)

@app.route('/aggregate_predict', methods=['GET'])
def aggregate_predict():
    # Faites des requêtes aux API des modèles individuels (remplacez les URL par les URLs réelles)
    model_urls = ['https://4319-89-30-29-68.ngrok-free.app', 'https://b187-89-30-29-68.ngrok-free.app', 'https://4926-89-30-29-68.ngrok-free.app']
    predictions = [get(url, params=request.args).json()['class_probabilities'] for url in model_urls]

    # Agrégez les prédictions (ici, on fait une moyenne)
    aggregated_prediction = aggregate_predictions(predictions)

    # Créez une réponse avec la prédiction consolidée
    response = {'aggregated_prediction': aggregated_prediction}
    
    return jsonify(response)

def aggregate_predictions(predictions):
    # Implémentez votre logique d'agrégation ici (moyenne, médiane, etc.)
    # Par exemple, moyenne des probabilités pour chaque classe
    aggregated_probabilities = [sum(probability['probability'] for prediction in predictions) / len(predictions) for probability in predictions[0]]

    # Créez la prédiction agrégée sous forme de dictionnaire
    aggregated_prediction = [{'class': prediction['class'], 'probability': probability} for prediction, probability in zip(predictions[0], aggregated_probabilities)]

    return aggregated_prediction

if __name__ == '_main_':
    app.run(host='0.0.0.0', port=5000)