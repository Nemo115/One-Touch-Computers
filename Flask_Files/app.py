from flask import Flask, render_template, request, redirect, flash, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "temp_key"
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "5fwja35"
app.config['MYSQL_DB'] = "one_touch_computersdb"

mysql = MySQL(app)

def select_search(name):
    return "SELECT * FROM customer_table WHERE name LIKE '%"+ name +"%'"

@app.route('/', methods =['GET', 'POST'])
def home():
    '''if request.method == 'POST':
        try:
            name = request.form['customerName']
            email = request.form['email']
            phone = request.form['phone']
            outID = -1

            cursor = mysql.connection.cursor()
            cursor.callproc('stdAddUser', (name, email, phone, outID))
            mysql.connection.commit()
            cursor.close()
        except:
            flash("Error: Unable to submit new entry, not connected to SQL database")'''
    return render_template('home.html')

@app.route('/customer_details', methods = ['GET', 'POST'])
def customer_details():   
    try:
        cur = mysql.connection.cursor()
        if request.method == 'POST':
            try:
                name = request.form['customerName']
                email = request.form['email']
                phone = request.form['phone']
                outID = -1

                cursor = mysql.connection.cursor()
                cursor.callproc('stdAddUser', (name, email, phone, outID))
                mysql.connection.commit()
                cursor.close()
            except:
                flash("Error: Unable to submit new entry, not connected to SQL database")
        if request.method == 'GET':#search bar entered
            search_bar = "search_customerName"
            if request.args.get(search_bar) != None:#if the argument is in searchbar
                #sqlString = "SELECT * FROM customer_table WHERE name LIKE '%"+ request.args.get("search_customerName") +"%'"
                customers = cur.execute(select_search(request.args.get(search_bar)))
                connection = True
                if customers > 0:
                    customer_details = cur.fetchall()
                    return render_template('customers.html', customerDetails = customer_details, connected = connection)
        customers = cur.execute("SELECT * FROM customer_table")
        connection = True
        if customers > 0:
            customer_details = cur.fetchall()
            return render_template('customers.html', customerDetails = customer_details, connected = connection)
    except:
        flash("Error: Database unavailable. Not connected to MySQL Database Server")
        return render_template('customers.html', connected = connection)

@app.route('/page_3')
def page_3():
    connection = False #validation for sql connection
    try:
        cur = mysql.connection.cursor()
        customers = cur.execute("SELECT * FROM job_table")
        connection = True
        if customers > 0:
            customer_details = cur.fetchall()
            return render_template('page3.html', orderDetails = customer_details, connected = connection)
    except:
        flash("Error: Database unavailable. Not connected to MySQL Database Server")
        return render_template('page3.html', connected = connection)
    '''if request.method == 'POST':
        try:
            name = request.form['customerName']
            email = request.form['email']
            phone = request.form['phone']
            outID = -1

            cursor = mysql.connection.cursor()
            cursor.callproc('stdAddUser', (name, email, phone, outID))
            mysql.connection.commit()
            cursor.close()
        except:
            flash("Error: Unable to submit new entry, not connected to SQL database")'''

@app.route('/page_4')
def page_4():
    return render_template('page4.html')

if __name__ == "__main__":
    app.run(debug = True)

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="5fwja35"
)

print(mydb)