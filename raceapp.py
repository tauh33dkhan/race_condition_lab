from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'test'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'coupon_demo'

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT code FROM coupons")
    valid_coupons = [row[0] for row in cur.fetchall()]
    return render_template('index.html', valid_coupons=valid_coupons)

@app.route('/apply_coupon', methods=['POST'])
def apply_coupon():
    coupon_code = request.form.get('coupon_code')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM used_coupons WHERE code = %s", (coupon_code,))
    used_coupon = cur.fetchone()
    print(used_coupon)
    if used_coupon:
        return "Coupon has already been used!"
    cur.execute("SELECT * FROM coupons WHERE code = %s", (coupon_code,))
    valid_coupon = cur.fetchone()

    if not valid_coupon:
        return "Invalid coupon code!"

    # Simulate a delay to make the race condition more likely
    import time
    time.sleep(1)

    try:
        cur.execute("INSERT INTO used_coupons (code) VALUES (%s)", (coupon_code,))
        mysql.connection.commit()  # Commit the transaction
    except Exception as e:
        print(f"Error: {e}")

    return "Coupon applied successfully!"
if __name__ == '__main__':
    app.run(debug=False)
