from flask import Flask
from flask import render_template
from flask import request
import sqlite3

app = Flask(__name__)



@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')



@app.route('/viewAllProducts', methods=['GET'])
def viewAllProducts():

    conn = sqlite3.connect('./db/products.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    conn.close()

    return render_template('viewAllProducts.html', products=products)



@app.route('/createNewProduct', methods=['GET', 'POST'])
def createNewProduct():

    if request.method == 'GET':

        return render_template('createNewProduct.html')
    
    elif request.method == 'POST':
        
        sku_code = request.form['sku_code']
        product_name = request.form['product_name']        
        product_description = request.form['product_description']
        brand = request.form['brand']
        model = request.form['model']
        category = request.form['category']
        quantity_on_hand = request.form['quantity_on_hand']
        unit_price = request.form['unit_price']

        conn = sqlite3.connect('./db/products.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO products (sku_code, product_name, product_description, brand, model, category, quantity_on_hand, unit_price)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (sku_code, product_name, product_description, brand, model, category, quantity_on_hand, unit_price))
        conn.commit()
        conn.close()

        return 'Product created with new Product ID: {} <a href="/">Home</a>'.format(cursor.lastrowid)



@app.route('/updateProduct/<product_id>', methods=['GET', 'POST'])
def updateProduct(product_id):

    if request.method == 'GET':

        conn = sqlite3.connect('./db/products.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products WHERE product_id = ?', (product_id,))
        product = cursor.fetchone()
        conn.close()

        return render_template('updateProduct.html', product=product)
    
    elif request.method == 'POST':

        sku_code = request.form['sku_code']
        product_name = request.form['product_name']        
        product_description = request.form['product_description']
        brand = request.form['brand']
        model = request.form['model']
        category = request.form['category']
        quantity_on_hand = request.form['quantity_on_hand']
        unit_price = request.form['unit_price']

        conn = sqlite3.connect('./db/products.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE products
            SET sku_code = ?, product_name = ?, product_description = ?, brand = ?, model = ?, category = ?, quantity_on_hand = ?, unit_price = ?
            WHERE product_id = ?
        ''', (sku_code, product_name, product_description, brand, model, category, quantity_on_hand, unit_price, product_id))
        conn.commit()
        conn.close()

        return 'Product updated successfully <a href="/">Home</a>'



@app.route('/deleteProduct/<product_id>', methods=['GET', 'POST'])
def deleteProduct(product_id):

    if request.method == 'GET':

        conn = sqlite3.connect('./db/products.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products WHERE product_id = ?', (product_id,))
        product = cursor.fetchone()
        conn.close()

        return render_template('deleteProduct.html', product=product)
    
    elif request.method == 'POST':

        conn = sqlite3.connect('./db/products.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM products WHERE product_id = ?', (product_id,))
        conn.commit()
        conn.close()

        return 'Product deleted successfully <a href="/">Home</a>'
