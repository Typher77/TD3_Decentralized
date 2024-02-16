from flask import Flask

app = Flask(__name__)

debut-product

# Define a route that responds with "Hello, World!"
=======
 main
@app.route('/')
def hello_world():
    return 'Hello World!'

debut-product

# Run the server
=======
 main
if __name__ == '__main__':
    app.run(host='localhost', port=3001)
