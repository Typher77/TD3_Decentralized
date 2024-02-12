from flask import Flask, jsonify

# Create an instance of Flask app
app = Flask(__name__)

# Define a route that responds with the URL of the server
@app.route('/getServer')
def get_server():
    server_url = 'localhost:3001'  # Assuming the server runs on the same machine
    return jsonify({"code": 200, "server": server_url})

# Run the DNS registry server
if __name__ == '__main__':
    app.run(host='localhost', port=3002)
