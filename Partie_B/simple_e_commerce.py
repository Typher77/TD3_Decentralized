from flask import Flask, jsonify,request
import sqlite3

app = Flask(__name__)



def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def hello_world():
    return '''<h1>Welcome to our simple e-commerce app</h1>
            <h1>To test the different routes, you can use Postmann</h1>

'''

# get products
@app.route('/products', methods=['GET'])
def get_products():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM products ORDER BY product_id")
   
    products = cursor.fetchall()
    conn.close()

    return jsonify([dict(row) for row in products])


# get products/id 
@app.route('/products/:<int:id>', methods=['GET'])
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
@app.route('/products', methods=['POST'])
def add_product():
    data=request.get_json()
   
    name = data['product_name']
    description = data['product_description']
    price = data['product_price']
    category = data['category']
    inStock = data['inStock']

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
        
              
# put products
@app.route('/products/:<int:id>', methods=['PUT'])
def put_product(id):
   data=request.get_json()
   
   name = data['product_name']
   description = data['product_description']
   price = data['product_price']
   category = data['category']
   inStock = data['inStock']
   
   conn = get_db_connection()
   cursor = conn.cursor()
   
   cursor.execute('''
                  UPDATE products SET product_name=?, product_description= ?, product_price= ?, category = ?, inStock= ? WHERE product_id = ?
                  ''', (name, description, price, category, inStock,id))
   
   conn.commit()
   cursor.execute("SELECT * FROM products WHERE product_id = ?", (id,))
   
   products = cursor.fetchall()
   conn.close()

   return jsonify([dict(row) for row in products])

# delete products
@app.route('/products/:<int:id>', methods=['DELETE'])
def delete_product(id):
    
    conn = get_db_connection()
    cursor = conn.cursor()
   
    cursor.execute('''
                   DELETE FROM products WHERE product_id = ?
                  ''', (id,))
   
    conn.commit()
    conn.close()
    return ' The product was deleted '

    

if __name__ == '__main__':
    app.run(host='localhost', port=3001)
