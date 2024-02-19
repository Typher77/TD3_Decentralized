# Q1: Develop diverse predictive models targeting the selected dataset. Each group member should create a distinct model.

We all created different models. Here's an example installation guide:

# Iris Prediction API

This Flask application provides a simple API for predicting Iris flower varieties based on input features.

## Getting Started

### Prerequisites
Clone this repository to your local machine:
git clone https://github.com/Typher77/TD3_Decentralized


Navigate to the project directory:
cd <project-directory>



Make sure you have Python and pip installed. You can install the required dependencies using:

```
pip install -r requirements.txt
```

## Running the Application
To run the Flask application, use the following command:

```
python main_heddy.py
```
The application will be accessible at http://yourdomain/

## Making Predictions
You can make predictions by sending a GET request to the /predict endpoint with the input parameters. 
For example:
```
curl "http://127.0.0.1:5000/predict?sepal.length=5.1&sepal.width=3.5&petal.length=1.4&petal.width=0.2"
```
## Example Response
```
{
  "class_probabilities": [
  
    {"class": "Setosa", "probability": 0.9},
    
    {"class": "Versicolor", "probability": 0.05},
    
    {"class": "Virginica", "probability": 0.05}
    
  ]
}
```



# Q2: Generate a consensus prediction by averaging outputs from the group's models, using tools like ngrok for inter-computer connectivity. Assess the performance of this aggregated meta-model.

To address this question, we implemented the code provided in question 2. The principle was that each member of the group trained their model locally on their machine, and thanks to ngrok, it allowed us to access each other's models remotely. 

<img width="637" alt="Capture d’écran 2024-02-18 à 23 13 58" src="https://github.com/Typher77/TD3_Decentralized/assets/120495158/c69564fa-0d30-4af8-92d9-392a63743d2e">

Finally, all that was left was to display them in a user-friendly manner and create an average of the different predictions.

<img width="472" alt="Capture d’écran 2024-02-12 à 15 13 23" src="https://github.com/Typher77/TD3_Decentralized/assets/120495158/2c189201-3f19-4e48-9624-579883e75a6c">

# Q3: Introduce a weighting system to refine the meta-model's predictions. Weights, ranging from 0 to 1, are adjusted with each prediction batch to reflect the accuracy of individual models relative to the group consensus.

For this question, we all had to modify our Flask applications to also return the precision. Thus, the output of question 1 becomes:

<img width="1145" alt="Capture d’écran 2024-02-18 à 23 15 42" src="https://github.com/Typher77/TD3_Decentralized/assets/120495158/c0f599a0-b663-49ea-8104-0bdcbc73a5f4">

So, by having the precision for each species of each model, we were able to implement a weighting system that allows us to ensure our model is better. For example, for the comparison of two models, we have this result:

<img width="441" alt="Capture d’écran 2024-02-18 à 23 35 35" src="https://github.com/Typher77/TD3_Decentralized/assets/120495158/1da0f875-f136-4eaa-851d-2a1866252f15">


