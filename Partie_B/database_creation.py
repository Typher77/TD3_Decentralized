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



conn.commit()


# Close the connection
conn.close()

print("Database and table created successfully!")
