from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "5fwja35"
app.config['MYSQL_DB'] = "one_touch_computersdb"

mysql = MySQL(app)

@app.route('/', methods =['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form['customerName']
        email = request.form['email']
        phone = request.form['phone']
        outID = -1;

        cursor = mysql.connection.cursor()
        cursor.callproc('stdAddUser', (name, email, phone, outID))
        #outputN = cursor.stored_results()
        mysql.connection.commit()
        cursor.close()
    return render_template('home.html')

@app.route('/customer_details')
def customer_details():
    cur = mysql.connection.cursor()
    customers = cur.execute("SELECT * FROM customer_table")

    if customers > 0:
        customer_details = cur.fetchall()
        return render_template('customers.html', customerDetails = customer_details)

if __name__ == "__main__":
    app.run(debug = True)

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="5fwja35"
)

print(mydb)