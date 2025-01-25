from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash
import mysql.connector


app = Flask(__name__)
app.secret_key = 'your_secret_key'  

# Database connection
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Rutu@3158',
            database='computerstore',
            port=3307
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None

users = {}
cart_items = []  # Initialize cart_items globally

# Example products data (you should fetch it from the database ideally)
products_data = {
    'monitor': [
        {'id': 1, 'name': 'Dell 24-inch FHD Monitor', 'price': '₹14500', 'image': 'images/monitor/Dell 24-Inch FHD 165Hz .jpg'},
        {'id': 2, 'name': 'HP 22-inch LED Monitor', 'price': '₹12500', 'image': 'images/monitor/Hp .jpg'},
        {'id': 3, 'name': 'LG UltraWide 29-inch Monitor', 'price': '₹18500', 'image': 'images/monitor/LG ultrawide.jpg'},
        {'id': 4, 'name': 'Samsung 27-inch Curved Monitor', 'price': '₹21000', 'image': 'images/monitor/Samsung 27-INCH .jpg'},
        {'id': 5, 'name': 'Acer Nitro 23.8-inch Monitor', 'price': '₹19500', 'image': 'images/monitor/Acer - Monitor PC Gaming 60 cm .jpg'},
        {'id': 6, 'name': 'ASUS TUF Gaming 27-inch Monitor', 'price': '₹24000', 'image': 'images/monitor/ASUS TUF Gaming 27” 1080p.jpg'},
        {'id': 7, 'name': 'BenQ 32-inch 4K Monitor', 'price': '₹35000', 'image': 'images/monitor/Benq 4k.jpg'},
        {'id': 8, 'name': 'MSI Optix 27-inch Gaming Monitor', 'price': '₹28000', 'image': 'images/monitor/MSI .jpg'},
        {'id': 9, 'name': 'ViewSonic 32-inch WQHD Monitor', 'price': '₹32000', 'image': 'images/monitor/Viewsonic Vp3481.jpg'},
        {'id': 10, 'name': 'Gigabyte AORUS 43-inch Monitor', 'price': '₹55000', 'image': 'images/monitor/Aorus.jpg'}
    ],
    'mouse': [
        {'id': 1, 'name': 'Logitech M90 Wired Mouse', 'price': '₹450', 'image': 'images/mouse/logetch m09.jpg'},
        {'id': 2, 'name': 'HP X1000 Wired Mouse', 'price': '₹500', 'image': 'images/mouse/hp x1000.jpg'},
        {'id': 3, 'name': 'Dell MS116 Optical Mouse', 'price': '₹550', 'image': 'images/mouse/dell ms116.jpg'},
        {'id': 4, 'name': 'Lenovo 300 USB Mouse', 'price': '₹600', 'image': 'images/mouse/lenevo 300.jpg'},
        {'id': 5, 'name': 'Zebronics Zeb-Transformer Mouse', 'price': '₹700', 'image': 'images/mouse/zebronic transformer.jpg'},
        {'id': 6, 'name': 'Corsair Harpoon RGB Mouse', 'price': '₹2000', 'image': 'images/mouse/corasir haproon.jpg'},
        {'id': 7, 'name': 'Logitech G502 Hero Mouse', 'price': '₹4000', 'image': 'images/mouse/logitech g502.jpg'},
        {'id': 8, 'name': 'SteelSeries Rival 600 Mouse', 'price': '₹7000', 'image': 'images/mouse/steelserie.jpg'},
        {'id': 9, 'name': 'Asus ROG Gladius III Gaming Mouse', 'price': '₹4000', 'image': 'images/mouse/Asus ROG Gladius III Gaming Mouse.jpg'},
        {'id': 10, 'name': 'Razer DeathAdder Essential Mouse', 'price': '₹1600', 'image': 'images/mouse/razer deathadder.jpg'},
    ],
    'cabinet': [
        {'id': 1, 'name': 'Corsair Carbide Series 100R', 'price': '₹3500', 'image': 'images/cabinet/corsair 100r.jpg'},
        {'id': 2, 'name': 'Cooler Master MasterBox Q300L', 'price': '₹4000', 'image': 'images/cabinet/masterQ300L.jpg'},
        {'id': 3, 'name': 'NZXT H510 Mid-Tower', 'price': '₹8000', 'image': 'images/cabinet/NZXT H510.jpg'},
        {'id': 4, 'name': 'Thermaltake Versa H18', 'price': '₹4200', 'image': 'images/cabinet/Thermaltake.jpg'},
        {'id': 5, 'name': 'Deepcool Matrexx 55 Mesh', 'price': '₹5500', 'image': 'images/cabinet/Deepcool x55.jpg'},
        {'id': 6, 'name': 'Antec NX210 Gaming Cabinet', 'price': '₹4700', 'image': 'images/cabinet/antec NX210.jpg'},
        {'id': 7, 'name': 'Lian Li O11 Dynamic', 'price': '₹11000', 'image': 'images/cabinet/lian li 011.jpg'},
        {'id': 8, 'name': 'Cooler Master TD500 Mesh', 'price': '₹9500', 'image': 'images/cabinet/Cooler master TD500.jpg'},
        {'id': 9, 'name': 'ASUS ROG Strix Helios GX601 ', 'price': '₹12500', 'image': 'images/cabinet/Asus Helois.jpg'},
        {'id': 10, 'name': 'Fractal Design Meshify 2', 'price': '₹14000', 'image': 'images/cabinet/meshify.jpg'}
    ],
    'graphiccard': [
        {'id': 1, 'name': 'Gigabyte NVIDIA GeForce GTX 1650', 'price': '₹18000', 'image': 'images/graphiccard/Giagabyte Nvdia 1650.jpg'},
        {'id': 2, 'name': 'ASROCK AMD Radeon RX 6600', 'price': '₹25000', 'image': 'images/graphiccard/Asrock 6600.jpg'},
        {'id': 3, 'name': 'MSI NVIDIA GeForce RTX 3060', 'price': '₹35000', 'image': 'images/graphiccard/msi 3060.jpg'},
        {'id': 4, 'name': 'ASUS AMD Radeon RX 6700 XT', 'price': '₹42000', 'image': 'images/graphiccard/Asus  RX 6700XT.jpg'},
        {'id': 5, 'name': 'GIGABYTE NVIDIA GeForce RTX 3070', 'price': '₹55000', 'image': 'images/graphiccard/Gigabyte 3070.jpg'},
        {'id': 6, 'name': 'AMD Radeon RX 6800 XT', 'price': '₹70000', 'image': 'images/graphiccard/Amd Radeon 6800 XT.jpg'},
        {'id': 7, 'name': 'NVIDIA GeForce RTX 3080', 'price': '₹85000', 'image': 'images/graphiccard/30810.jpg'},
        {'id': 8, 'name': 'NVIDIA GeForce RTX 4070', 'price': '₹95000', 'image': 'images/graphiccard/ZOTAC 4070.jpg'},
        {'id': 9, 'name': 'Sapphire Radeon RX 7900 XTX', 'price': '₹120000', 'image': 'images/graphiccard/Sapphire 7900XTX.jpg'},
        {'id': 10, 'name': 'Aorus NVIDIA GeForce RTX 4090', 'price': '₹180000', 'image': 'images/graphiccard/Aorus 4090.jpg'}
    ],
    'keyboard': [
    {'id': 1, 'name': 'Dell KB216 Wired Keyboard', 'price': '₹700', 'image': 'images/keyboard/dell kb522.jpg'},
    {'id': 2, 'name': 'HP 150 Wired Keyboard', 'price': '₹800', 'image': 'images/keyboard/Hp 150.jpg'},
    {'id': 3, 'name': 'Logitech K120 Wired Keyboard', 'price': '₹600', 'image': 'images/keyboard/logitech K120.jpg'},
    {'id': 4, 'name': 'Redragon K552 Mechanical Keyboard', 'price': '₹2500', 'image': 'images/keyboard/Redragon k522.jpg'},
    {'id': 5, 'name': 'Cosmic Byte CB-GK-32 Mechanical Gaming Keyboarard', 'price': '₹1900', 'image':'images/keyboard/Cosmic CB_GK.jpg'},
    {'id': 6, 'name': 'Zebronics Zeb-KM2100 Wired Keyboard', 'price': '₹750', 'image':'images/keyboard/Zebronic KM2100.jpg'},
    {'id': 7, 'name': 'Razer Cynosa V2 RGB Gaming Keyboard', 'price': '₹4000', 'image':'images/keyboard/Razee Cynosa v2.jpg'},
    {'id': 8, 'name': 'Microsoft Wired Keyboard 600', 'price': '₹1200', 'image': 'images/keyboard/Microsoft keyboard 600.jpg'},
    {'id': 9, 'name': 'ASUS TUF Gaming K1 Keyboard', 'price': '₹1300', 'image': 'images/keyboard/Asus tuf keyboard.jpg'},
    {'id': 10, 'name': 'MSI VIGOR GK20 Gaming Keyboard', 'price': '₹3500', 'image': 'images/keyboard/MSI VIGOR.jpg'}
],
'processor': [
    {'id': 1, 'name': 'Intel Core i3-14100', 'price': '₹11000', 'image': '/images/processor/i3 14100.jpg'},
    {'id': 2, 'name': 'AMD Ryzen 3 4100G', 'price': '₹10000', 'image': 'images/processor/Ryzen 3 4100U.jpg'},
    {'id': 3, 'name': 'Intel Core i5-14600K', 'price': '₹30000', 'image': 'images/processor/i5 14600k.jpg'},
    {'id': 4, 'name': 'AMD Ryzen 5 7600X', 'price': '₹21000', 'image': 'images/processor/Ryzen 5 57600x.jpg'},
    {'id': 5, 'name': 'Intel Core i7-14700K', 'price': '₹35000', 'image': 'images/processor/i7 14700k.jpg'},
    {'id': 6, 'name': 'AMD Ryzen 7 7700X', 'price': '₹30000', 'image': 'images/processor/7 7700x.jpg'},
    {'id': 7, 'name': 'Intel Core i9-14900K', 'price': '₹42000', 'image': 'images/processor/i9 14900k .jpg'},
    {'id': 8, 'name': 'AMD Ryzen 9 9950X', 'price': '₹45000', 'image': 'images/processor/9 9950x.jpg'},
    {'id': 9, 'name': 'Intel Core i9-9980Xe Extreme Edition Processor', 'price': '₹50000', 'image': 'images/processor/i9 extreme.jpg'},
    {'id': 10, 'name': 'AMD Ryzen Threadripper Pro 5995WX Processor', 'price': '₹450000', 'image': 'images/processor/Threadrippwe 5995WX.jpg'}
]

}


@app.route('/')
def home():
    return render_template('computershop.html')  # Home page

# Login Route
from werkzeug.security import check_password_hash

@app.route('/login', methods=['GET', 'POST'])
def login():
    cursor = None  # Initialize cursor
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            connection = get_db_connection()
            if connection is None:
                flash('Failed to connect to the database', 'danger')
                return render_template('login.html')

            cursor = connection.cursor(dictionary=True)

            # Fetch user by username
            cursor.execute("SELECT * FROM customer WHERE username = %s", (username,))
            user = cursor.fetchone()

            if user and check_password_hash(user['password'], password):
                session['user_id'] = user['id']  # Store user session
                flash('Login successful!', 'success')
                return redirect(url_for('home'))  # Update with your home page route
            else:
                flash('Invalid username or password', 'danger')

        except mysql.connector.Error as err:
            flash(f"Database error: {err}", 'danger')
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        hashed_password = generate_password_hash(password)

        connection = None
        cursor = None

        try:
            connection = get_db_connection()
            if connection is None:
                flash('Failed to connect to the database', 'danger')
                return render_template('signup.html')

            cursor = connection.cursor(dictionary=True)

            # Check if the username already exists
            cursor.execute("SELECT * FROM customer WHERE username=%s", (username,))
            existing_user = cursor.fetchone()

            if existing_user:
                flash('Username already exists', 'danger')
            else:
                # Insert user without an address
                cursor.execute(
                    "INSERT INTO customer (username, email, password) VALUES (%s, %s, %s)",
                    (username, email, hashed_password)
                )
                connection.commit()
                flash('Signup successful! You can now log in.', 'success')
                return redirect(url_for('login'))
        except mysql.connector.Error as err:
            flash(f"Database error: {err}", 'danger')
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    return render_template('signup.html')


@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        if 'user_id' not in session:
            flash("You must be logged in to proceed with payment.", "danger")
            return redirect(url_for('login'))

        customer_id = session['user_id']  # Retrieve customer_id from session
        name = request.form['name']
        contact = request.form['contact']
        email = request.form['email']
        address = request.form['address']
        payment_method = request.form['payment_method']
        details = {}

        if payment_method == 'credit_card':
            details['account_number'] = request.form['account_number']
            details['cardholder_name'] = request.form['cardholder_name']
            details['card_number'] = request.form['card_number']
            details['card_expiry'] = request.form['card_expiry']
            details['card_cvc'] = request.form['card_cvc']
        elif payment_method == 'paypal':
            details['upi_id'] = request.form['upi_id']
        elif payment_method == 'cash_on_delivery':
            details = {}

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO payments (customer_id, name, contact, email, address, payment_method, details, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
            """, (customer_id, name, contact, email, address, payment_method, str(details)))

            connection.commit()

            # Redirect with a success flag
            return redirect(url_for('payment', success=True))

        except mysql.connector.Error as err:
            flash(f"Database error: {err}", 'danger')
        finally:
            cursor.close()
            connection.close()

    success = request.args.get('success', 'false').lower() == 'true'
    return render_template('payment.html', success=success)



@app.route('/cart', methods=['GET'])
def cart():
    user_cart = session.get('cart_items', [])
    total_price = sum(item['price'] * item['quantity'] for item in user_cart)
    return render_template('cart.html', cart_items=user_cart, total_price=total_price)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    price = request.form['price'].replace('₹', '').replace(',', '')  # Remove ₹ and commas
    item = {
        'id': request.form['id'],
        'name': request.form['name'],
        'price': float(price),
        'quantity': int(request.form['quantity'])
    }

    cart_items = session.get('cart_items', [])

    # Check if the item is already in the cart
    existing_item = next((x for x in cart_items if x['id'] == item['id']), None)
    if existing_item:
        existing_item['quantity'] += item['quantity']
    else:
        cart_items.append(item)

    session['cart_items'] = cart_items

    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<item_name>', methods=['POST'])
def remove_from_cart(item_name):
    cart_items = session.get('cart_items', [])
    cart_items = [item for item in cart_items if item['name'] != item_name]
    session['cart_items'] = cart_items

    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET'])
def checkout():
    cart_items = session.get('cart_items', [])
    total_price = sum(item['price'] * item['quantity'] for item in cart_items)

    if 'user_id' in session:
        user_id = session['user_id']
        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            for item in cart_items:
                cursor.execute("""
                    INSERT INTO cart (user_id, item_id, quantity)
                    VALUES (%s, %s, %s)
                """, (user_id, item['id'], item['quantity']))

            connection.commit()
        except mysql.connector.Error as err:
            flash(f"Database error: {err}", 'danger')
        finally:
            cursor.close()
            connection.close()

        return redirect(url_for('payment'))

    else:
        flash("You must be logged in to checkout", 'warning')
        return redirect(url_for('login'))


from flask import render_template, request, redirect, url_for, session, flash
import mysql.connector

# Admin Login Route
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check admin credentials (hardcoded for simplicity; use a database for real apps)
        if username == "admin" and password == "admin@123":  # Replace with secure logic
            session['admin_logged_in'] = True
            flash('Admin login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid admin credentials!', 'danger')

    return render_template('admin_login.html')

# Admin Logout Route
@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('admin_login'))

# Admin Dashboard
@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        flash('Please log in as admin to access this page', 'danger')
        return redirect(url_for('admin_login'))

    customers = []
    payments = []

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Fetch all customers
        cursor.execute("SELECT id, username, email FROM customer")
        customers = cursor.fetchall()

        # Fetch all payments
        cursor.execute("SELECT id, name, email, payment_method, address, details, created_at FROM payments")
        payments = cursor.fetchall()

# Fetch purchased products for each customer
        for customer in customers:
            cursor.execute("""
                SELECT 
                    p.id AS product_id, 
                    p.name AS product_name,
                    p.category,  -- Add category to query
                    op.quantity, 
                    op.price 
                FROM 
                    orders o 
                JOIN 
                    order_products op ON o.id = op.order_id 
                JOIN 
                    products p ON op.product_id = p.id 
                WHERE 
                    o.customer_id = %s
            """, (customer['id'],))
            customer['purchased_products'] = cursor.fetchall()

    except mysql.connector.Error as err:
        flash(f"Database error: {err}", 'danger')
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    return render_template('admin_dashboard.html', customers=customers, payments=payments)

# Add Customer
@app.route('/admin/add_customer', methods=['POST'])
def add_customer():
    if not session.get('admin_logged_in'):
        flash('Unauthorized action!', 'danger')
        return redirect(url_for('admin_login'))

    username = request.form.get('username')
    email = request.form.get('email')

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("INSERT INTO customer (username, email) VALUES (%s, %s)", (username, email))
        connection.commit()
        flash('Customer added successfully!', 'success')

    except mysql.connector.Error as err:
        flash(f"Database error: {err}", 'danger')
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    return redirect(url_for('admin_dashboard'))


# Update Customer
@app.route('/admin/update_customer/<int:customer_id>', methods=['POST'])
def update_customer(customer_id):
    if not session.get('admin_logged_in'):
        flash('Unauthorized action!', 'danger')
        return redirect(url_for('admin_login'))

    username = request.form.get('username')
    email = request.form.get('email')
    address = request.form.get('address')

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE customer
            SET username = %s, email = %s, address = %s
            WHERE id = %s
        """, (username, email, address, customer_id))
        connection.commit()
        flash('Customer updated successfully!', 'success')

    except mysql.connector.Error as err:
        flash(f"Database error: {err}", 'danger')
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    return redirect(url_for('admin_dashboard'))

# Delete Customer
@app.route('/admin/delete_customer/<int:customer_id>', methods=['POST'])
def delete_customer(customer_id):
    if not session.get('admin_logged_in'):
        flash('Unauthorized action!', 'danger')
        return redirect(url_for('admin_login'))

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Delete customer
        cursor.execute("DELETE FROM customer WHERE id = %s", (customer_id,))
        connection.commit()
        flash('Customer deleted successfully!', 'success')

    except mysql.connector.Error as err:
        flash(f"Database error: {err}", 'danger')
    finally:
        if cursor:
            cursor.close()
        if connection:  
            connection.close()

    return redirect(url_for('admin_dashboard'))


@app.route('/monitor', methods=['GET'])
def monitor():
    return render_template('monitor.html', products=products_data['monitor'])

@app.route('/mouse', methods=['GET'])
def mouse():
    return render_template('mouse.html', products=products_data['mouse'])

@app.route('/cabinet', methods=['GET'])
def cabinet():
    return render_template('cabinet.html', products=products_data['cabinet'])

@app.route('/keyboard', methods=['GET'])
def keyboard():
    return render_template('keyboard.html', products=products_data['keyboard'])

@app.route('/graphiccard', methods=['GET'])
def graphiccard():
    return render_template('graphiccard.html', products=products_data['graphiccard'])

@app.route('/processor', methods=['GET'])
def processor():
    return render_template('processor.html', products=products_data['processor'])

if __name__ == '__main__':
    app.run(debug=True)
