from flask import Flask

# Create an instance of Flask app
app = Flask(__name__)


# Define a route that responds with "Hello, World!"
@app.route('/')
def hello_world():
    return 'Hello World!'


# Run the server
if __name__ == '__main__':
    app.run(host='localhost', port=3001)
