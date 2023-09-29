from flask import Flask, render_template, request, redirect, url_for
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

    try:
        # Check if the coupon has already been used
        cur.execute("SELECT * FROM used_coupons WHERE code = %s FOR UPDATE", (coupon_code,))
        used_coupon = cur.fetchone()

        if used_coupon:
            return "Coupon has already been used!"

        # Check if the coupon is valid
        cur.execute("SELECT * FROM coupons WHERE code = %s FOR UPDATE", (coupon_code,))
        valid_coupon = cur.fetchone()

        if not valid_coupon:
            return "Invalid coupon code!"

        # Mark the coupon as used
        cur.execute("INSERT INTO used_coupons (code) VALUES (%s)", (coupon_code,))

        # Commit the transaction
        mysql.connection.commit()
    except Exception as e:
        # Rollback the transaction in case of any error
        mysql.connection.rollback()
        return f"Error: {e}"
    finally:
        # Always close the cursor
        cur.close()

    return "Coupon applied successfully!"
if __name__ == '__main__':
    app.run(debug=False)
