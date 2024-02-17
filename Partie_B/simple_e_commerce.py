from flask import Flask, jsonify,request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)



def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def hello_world():
    return '''<h1>Welcome to our simple e-commerce app</h1>
            <h1>products: get the list of products</h1>
            <h1>products/id : get the product identified by its id</h1>
            <h1>add product: POST product</h1>

'''

# get products
@app.route('/products', methods=['GET'])
def get_products():
    conn = get_db_connection()
    cursor = conn.cursor()
    
   
    cursor.execute("SELECT * FROM products ORDER BY inStock DESC")
   
    products = cursor.fetchall()
    conn.close()

    return jsonify([dict(row) for row in products])


# get products/id 
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

#post products
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    # handle the POST request
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        category = request.form.get('category')
        inStock = request.form.get('inStock')
        
        #creating the new object
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT count(*) FROM products")
        product_id = cursor.fetchone()[0]

        cursor.execute('''
    INSERT INTO Products(product_id, product_name, product_description, product_price, category, inStock ) VALUES 
(?,?,?,?,?,?)''', (product_id + 1, name, description, price, category, inStock))
        
        conn.commit()
        cursor.execute("SELECT * FROM products WHERE product_id = ?", (product_id+1,))
   
        products = cursor.fetchall()
        conn.close()

        return jsonify([dict(row) for row in products])
       
       # form to get the new object information
    return '''
              <form method="POST">
                  <div><label>product name: <input type="text" name="name"></label></div>
                  <div><label>product description: <input type="text" name="description"></label></div>
                  <div><label>product price : <input type="number" name="price"></label></div>
                  <div><label>product category: <input type="text" name="category"></label></div>
                  <div><label>product stock state : <input type="number" name="inStock"></label></div>
                  <input type="submit" value="Submit">
              </form>'''

if __name__ == '__main__':
    app.run(host='localhost', port=3001)
