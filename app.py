from flask import Flask, render_template
import psycopg2

app = Flask(__name__)  # ✅ Define the app here

# ✅ Database connection
conn = psycopg2.connect(
    dbname="database_db",
    user="postgres",
    password="bohlokoa2706",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

# ✅ Routes below this point
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/customers')
def customers():
    try:
        cur.execute("SELECT * FROM customer")
        data = cur.fetchall()
        print("Customer data:", data)
        return render_template('customers.html', customers=data)
    except Exception as e:
        conn.rollback()
        return f"Error fetching customer data: {e}"

@app.route('/inventory')
def inventory():
    try:
        cur.execute("SELECT * FROM product")
        data = cur.fetchall()
        print("Inventory data:", data)
        return render_template('inventory.html', inventory=data)
    except Exception as e:
        conn.rollback()
        return f"Error fetching inventory data: {e}"

@app.route('/sales')
def sales():
    try:
        cur.execute("SELECT * FROM sale")
        data = cur.fetchall()
        print("Sales data:", data)
        return render_template('sales.html', sales=data)
    except Exception as e:
        conn.rollback()
        return f"Error fetching sales data: {e}"

# ✅ Run the app
if __name__ == '__main__':
    app.run(debug=True)


@app.route('/product/<int:product_id>')
def product_detail(product_id):
    try:
        cur.execute("SELECT * FROM product WHERE ProductID = %s", (product_id,))
        product = cur.fetchone()
        if product:
            return f"""
                <h2>Product Details</h2>
                <p><strong>Name:</strong> {product[1]}</p>
                <p><strong>Brand:</strong> {product[2]}</p>
                <p><strong>Price:</strong> M{product[3]}</p>
                <p><strong>Stock Quantity:</strong> {product[4]}</p>
                <p><a href='/inventory'>← Back to Inventory</a></p>
            """
        else:
            return "Product not found."
    except Exception as e:
        conn.rollback()
        return f"Error loading product detail: {e}"

