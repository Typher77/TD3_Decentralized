from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/products', methods=['GET'])
def get_products():
    conn = get_db_connection()
    cursor = conn.cursor()
    
   
    cursor.execute("SELECT * FROM products ORDER BY inStock DESC")
   
    products = cursor.fetchall()
    conn.close()

    return jsonify([dict(row) for row in products])

@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE product_id = ?", (id,))
    product = cursor.fetchone()
    conn.close()

    if product:
        return jsonify(dict(product)), 200
    else:
        return jsonify({"error": "Product not found"}), 404


if __name__ == '__main__':
    app.run(host='localhost', port=3001)
