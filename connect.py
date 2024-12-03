from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)
DB_SERVER = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'esha'
DB_DATABASE = 'inventory'

def connect_to_database():
    return pymysql.connect(
        host=DB_SERVER,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_DATABASE
    )

def create_product_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Product (
            ProductID INT AUTO_INCREMENT PRIMARY KEY,
            SerialNumber INT UNIQUE,
            ProductName VARCHAR(255),
            Description TEXT,
            CategoryID INT,
            SupplierID INT,
            QuantityAvailable INT,
            Price DECIMAL(10, 2),
            FOREIGN KEY (CategoryID) REFERENCES Category(CategoryID),
            FOREIGN KEY (SupplierID) REFERENCES Supplier(SupplierID)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Category (
            CategoryID INT AUTO_INCREMENT PRIMARY KEY,
            CategoryName VARCHAR(255) NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Supplier (
            SupplierID INT AUTO_INCREMENT PRIMARY KEY,
            SupplierName VARCHAR(255),
            ContactInformation VARCHAR(255),
            Address TEXT
        )
    """)

@app.route('/')
def index():
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Product")
        products = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template('index.html', products=products)
    except Exception as e:
        return f'Error: {str(e)}'
@app.route('/add_product', methods=['POST'])
def add_product():
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        create_product_table(cursor)
        product_name = request.form['productName']
        description = request.form['description']
        category_id = request.form['category']
        supplier_id = request.form['supplier']
        quantity_available = request.form['quantity']
        price = request.form['price']
        sr = request.form['sr']
        cursor.execute('INSERT INTO Product (ProductName, Description, CategoryID, SupplierID, QuantityAvailable, Price, SerialNumber) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                       (product_name, description, category_id, supplier_id, quantity_available, price, sr))
        
        conn.commit()
        cursor.close()
        conn.close()
    
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.SerialNumber, p.ProductName, p.Description, c.CategoryName, s.SupplierName, p.QuantityAvailable, p.Price
            FROM Product p
            JOIN Category c ON p.CategoryID = c.CategoryID
            JOIN Supplier s ON p.SupplierID = s.SupplierID
        ''')

        products = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('index.html', products=products)  
    except Exception as e:
        return f'Error: {str(e)}'   
@app.route('/update_product', methods=['POST'])
def update_product():
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        product_name = request.form['productName']
        description = request.form['description']
        category_id = request.form['category']
        supplier_id = request.form['supplier']
        quantity_available = request.form['quantity']
        price = request.form['price']
        sr = request.form['sr']  
        cursor.execute("""
            UPDATE Product
            SET ProductName = %s, Description = %s, CategoryID = %s, SupplierID = %s, QuantityAvailable = %s, Price = %s
            WHERE SerialNumber = %s
        """, (product_name, description, category_id, supplier_id, quantity_available, price, sr))

        conn.commit()
        cursor.close()
        conn.close()
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.SerialNumber, p.ProductName, p.Description, c.CategoryName, s.SupplierName, p.QuantityAvailable, p.Price
            FROM Product p
            JOIN Category c ON p.CategoryID = c.CategoryID
            JOIN Supplier s ON p.SupplierID = s.SupplierID
        ''')

        products = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('index.html', products=products)  
    except Exception as e:
        return f'Error: {str(e)}' 
@app.route('/delete_product', methods=['POST'])
def delete_product():
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        sr = request.form['sr']
        cursor.execute("DELETE FROM Product WHERE SerialNumber = %s", (sr,))

        conn.commit()
        cursor.close()
        conn.close()

        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.SerialNumber, p.ProductName, p.Description, c.CategoryName, s.SupplierName, p.QuantityAvailable, p.Price
            FROM Product p
            JOIN Category c ON p.CategoryID = c.CategoryID
            JOIN Supplier s ON p.SupplierID = s.SupplierID
        ''')

        products = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('index.html', products=products)  
    except Exception as e:
        return f'Error: {str(e)}' 

@app.route('/products', methods=['GET', 'POST'])
def products():
    if request.method == 'POST':
        selected_category = request.form['category'] 
        try:
            conn = connect_to_database()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT p.SerialNumber, p.ProductName, p.Description, c.CategoryName, s.SupplierName, p.QuantityAvailable, p.Price
                FROM Product p
                JOIN Category c ON p.CategoryID = c.CategoryID
                JOIN Supplier s ON p.SupplierID = s.SupplierID
                WHERE p.CategoryID = %s
            ''', (selected_category,))
            products = cursor.fetchall()
            cursor.close()
            conn.close()
            return render_template('index.html', products=products) 
        except Exception as e:
            return f'Error: {str(e)}'
    else:
        try:
            conn = connect_to_database()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT p.SerialNumber, p.ProductName, p.Description, c.CategoryName, s.SupplierName, p.QuantityAvailable, p.Price
                FROM Product p
                JOIN Category c ON p.CategoryID = c.CategoryID
                JOIN Supplier s ON p.SupplierID = s.SupplierID
            ''')

            products = cursor.fetchall()
            cursor.close()
            conn.close()
            return render_template('index.html', products=products)  
        except Exception as e:
            return f'Error: {str(e)}'

if __name__ == '__main__':
    app.run(debug=True)
