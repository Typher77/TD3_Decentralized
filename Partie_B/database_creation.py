import sqlite3


conn = sqlite3.connect('database.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create the products table
cursor.execute('''
    CREATE TABLE Products (
        product_id INT PRIMARY KEY,
        product_name VARCHAR(255) NOT NULL,
        product_description TEXT,
        product_price DECIMAL(10, 2) NOT NULL,
        category VARCHAR(50),
	    inStock BOOLEAN NOT NULL
)
''')

cursor.execute('''
    CREATE TABLE Orders (
        order_id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        total_price DECIMAL(10, 2) NOT NULL,
        status VARCHAR(20) NOT NULL DEFAULT 'pending',
        FOREIGN KEY (user_id) REFERENCES Users(user_id)
    )
''')

cursor.execute('''
    CREATE TABLE Carts (
        cart_id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        total_price DECIMAL(10, 2) NOT NULL DEFAULT 0,
        status VARCHAR(20) NOT NULL DEFAULT 'active'
    )
''')

cursor.execute('''
    INSERT INTO Products(product_id, product_name, product_description, product_price, category, inStock ) VALUES 
(1,"pen","blue pen",3,"stationnery",True)
''')

cursor.execute('''
   INSERT INTO Products(product_id, product_name, product_description, product_price, category, inStock ) VALUES 
(2,"pencil","pencil",2.5,"stationnery",True)
''')

cursor.execute('''
   INSERT INTO Products(product_id, product_name, product_description, product_price, category, inStock ) VALUES 
(3,"glue","a tube of glue",4,"stationnery",False)
''')

cursor.execute('''
    INSERT INTO Orders (order_id, user_id, total_price, status)
    VALUES (1, 123, 15.0, "shipped")
''')

cursor.execute('''
    INSERT INTO Orders (order_id, user_id, total_price, status)
    VALUES (2, 456, 10.5, "pending")
''')

cursor.execute('''
    INSERT INTO Orders (order_id, user_id, total_price, status)
    VALUES (3, 789, 25.0, "delivered")
''')

cursor.execute('''
    INSERT INTO Carts (cart_id, user_id, total_price, status)
    VALUES (1, 123, 0.0, 'active')
''')

cursor.execute('''
    INSERT INTO Carts (cart_id, user_id, total_price, status)
    VALUES (2, 456, 0.0, 'active')
''')

cursor.execute('''
    INSERT INTO Carts (cart_id, user_id, total_price, status)
    VALUES (3, 789, 0.0, 'active')
''')

conn.commit()


# Close the connection
conn.close()

print("Database and table created successfully!")
