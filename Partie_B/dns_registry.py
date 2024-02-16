from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/getServer')
def get_server():
    server_url = 'localhost:3001'
    return jsonify({"code": 200, "server": server_url})

if __name__ == '__main__':
    app.run(host='localhost', port=3001)
