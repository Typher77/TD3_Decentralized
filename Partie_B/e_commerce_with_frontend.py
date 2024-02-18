from flask import Flask, jsonify,request, redirect, url_for,render_template
import sqlite3
from flask_bootstrap import Bootstrap

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

#home page
@app.route('/')
def hello_world():
    return render_template("home.html")



# get products
@app.route('/products', methods=['GET'])
def get_products():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM products ORDER BY product_id")
   
    products = cursor.fetchall()
    conn.close()

    
    return render_template("get_product.html", products=products )

        


# get products/id 
@app.route('/products_id', methods=['GET', 'POST'])
def get_product():
    if request.method== 'POST':
        
        id =request.form.get('id')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE product_id = ?", (id,))
        product = cursor.fetchone()
        conn.close()

        if product:
            return render_template("get_product_id.html",id=product[0], name=product[1],description=product[2],price= product[3], category=product[4],inStock=product[5] )
        else:
            return jsonify({"error": "Product not found"}), 404
    return render_template('get_id.html')

#post products
@app.route('/products_post', methods=['POST', 'GET'])
def add_product():
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
   
        product = cursor.fetchone()
        conn.close()

        return render_template("get_product_id.html",id=product[0], name=product[1],description=product[2],price= product[3], category=product[4],inStock=product[5] )

       
       # form to get the new object information
    return render_template("post_form.html")  
        
              
# put products
@app.route('/put_product', methods=['POST','GET'])
def put_product():
    if request.method == 'POST':
        id =request.form.get('id')
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        category = request.form.get('category')
        inStock = request.form.get('inStock')
        
        
        conn = get_db_connection()
        cursor = conn.cursor()
   
        cursor.execute('''
                  UPDATE products SET product_name=?, product_description= ?, product_price= ?, category = ?, inStock= ? WHERE product_id = ?
                  ''', (name, description, price, category, inStock,id))
   
        conn.commit()
        cursor.execute("SELECT * FROM products WHERE product_id = ?", (id,))
   
        product = cursor.fetchone()
        conn.close()
        return render_template("get_product_id.html",id=product[0], name=product[1],description=product[2],price= product[3], category=product[4],inStock=product[5] )


    return render_template('put_form.html')

# delete products
@app.route('/del_products', methods=['DELETE', 'GET', 'POST'])
def delete_product():
    if request.method == 'POST':
        id= request.form.get('id')
        conn = get_db_connection()
        cursor = conn.cursor()
   
        cursor.execute('''
                   DELETE FROM products WHERE product_id = ?
                  ''', (id,))
   
        conn.commit()
        conn.close()
        return ' The product was deleted '
    
    return render_template('delete_form.html')

    

if __name__ == '__main__':
    app.run(host='localhost', port=3001)
