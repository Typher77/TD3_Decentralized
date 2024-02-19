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

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()

    user_id = data.get('user_id')
    products = data.get('products', [])
    total_price =data.get('total_price')
    status = 'pending'

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO orders (user_id, total_price, status) VALUES (?, ?, ?)
    ''', (user_id, total_price, status))

    order_id = cursor.lastrowid

    for product in products:
        product_id = product.get('product_id')
        quantity = product.get('quantity')
        cursor.execute('''
            INSERT INTO orders (order_id, product_id, quantity) VALUES (?, ?, ?)
        ''', (order_id, product_id, quantity))

    conn.commit()

    cursor.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,))
    order = cursor.fetchone()

    conn.close()

    return jsonify({
        "order_id": order["order_id"],
        "user_id": order["user_id"],
        "total_price": order["total_price"],
        "status": order["status"]
    })    

@app.route('/orders/<int:user_id>', methods=['GET'])
def get_user_orders(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM orders WHERE user_id = ?", (user_id,))
    orders = cursor.fetchall()

    conn.close()

    return jsonify([{
        "order_id": order["order_id"],
        "user_id": order["user_id"],
        "total_price": order["total_price"],
        "status": order["status"]
    } for order in orders])

@app.route('/cart/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT cart.user_id, cart.product_id, products.product_name, cart.quantity, products.product_price
        FROM cart
        JOIN products ON cart.product_id = products.product_id
        WHERE cart.user_id = ?
    ''', (user_id,))

    cart_contents = cursor.fetchall()

    conn.close()

    total_price = sum(item["product_price"] * item["quantity"] for item in cart_contents)

    return jsonify({
        "user_id": user_id,
        "cart_contents": cart_contents,
        "total_price": total_price
    })

@app.route('/cart/<int:user_id>/item/<int:product_id>', methods=['DELETE'])
def remove_from_cart(user_id, product_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        DELETE FROM cart WHERE user_id = ? AND product_id = ?
    ''', (user_id, product_id))

    conn.commit()
    
    cursor.execute("SELECT * FROM products WHERE product_id = ?", (product_id,))
    product = cursor.fetchone()

    conn.close()

    return jsonify({
        "user_id": user_id,
        "product_id": product["product_id"],
        "product_name": product["product_name"],
        "message": "Product removed from cart successfully."
    })

if __name__ == '__main__':
    app.run(host='localhost', port=3001)
