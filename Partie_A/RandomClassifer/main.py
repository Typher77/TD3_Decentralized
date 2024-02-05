import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

df = pd.read_csv('iris.csv', sep=',')

X = df.drop('variety', axis=1)
y = df['variety']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.8, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f'Model Accuracy: {accuracy}')



from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/predict', methods=['GET'])
def predict():
    args = request.args
    input_data = [[float(args['sepal.length']), float(args['sepal.width']), float(args['petal.length']), float(args['petal.width'])]]
    
    # Utiliser predict_proba au lieu de predict
    probabilities = model.predict_proba(input_data).tolist()[0]
    
    # Récupérer les noms de classe du modèle
    class_names = model.classes_
    
    # Créer une liste de dictionnaires avec le nom de la classe et sa probabilité
    class_probabilities = [{'class': class_name, 'probability': probability} for class_name, probability in zip(class_names, probabilities)]
    
    # Créer une réponse avec la liste de dictionnaires
    response = {'class_probabilities': class_probabilities}
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)