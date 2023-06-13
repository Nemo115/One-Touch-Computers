'''
The Following is a web application for sorting and managing customer data and company data.
Each page is written in the method and the corresponding html file. 
Each page functions under base.html through the use of blocks (Flask's feature of python code within html).

'''

from flask import Flask, render_template, request, redirect, flash, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "temp_key"
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "5fwja35"
app.config['MYSQL_DB'] = "one_touch_computersdb"

mysql = MySQL(app)

def select_search(bar, name, table):
    return f"SELECT * FROM {table} WHERE {name} LIKE \'%{bar}%\'"
@app.route('/', methods =['GET', 'POST'])
def home():
    connection = False
    try:
        cur = mysql.connection.cursor()
        data = cur.execute("SELECT * FROM customer_table")
        connection = True
        if data > 0:
            customer_details = cur.fetchall()
            return render_template('home.html', customerDetails = customer_details, connected = connection)
        pass
    except:
        flash("Error: Database unavailable. Not connected to MySQL Database Server")
        return render_template('home.html', connected = connection)

@app.route('/customer_details', methods = ['GET', 'POST'])
def customer_details(): 
    connection = False
    try:
        cur = mysql.connection.cursor()
        if request.method == 'POST':
            try:
                try:
                    customerID = request.form['customerID']
                    name = request.form['edit_cust_name']
                    email = request.form['edit_cust_email']
                    phone = request.form['edit_cust_phone']
                    cur.callproc('std_edit_cust', (customerID, name, email, phone))
                except:
                    name = request.form['customerName']
                    email = request.form['email']
                    phone = request.form['phone']
                    outID = -1
                    cur.callproc('stdAddUser', (name, email, phone, outID))
                mysql.connection.commit()
            except:
                flash("Error: Unable to submit new entry, not connected to SQL database")

        if request.method == 'GET':#search bar entered
            search_bar = "search_customerName"#defining searchBar
            if request.args.get(search_bar) != None:#if the argument is in searchbar
                #sqlString = "SELECT * FROM customer_table WHERE name LIKE '%"+ request.args.get("search_customerName") +"%'"
                customers = cur.execute(select_search(request.args.get(search_bar), 'name', 'customer_table'))
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

@app.route('/job_data', methods = ['GET', 'POST'])
def jobs():
    connection = False #validation for sql connection
    try:
        cur = mysql.connection.cursor()
        if request.method == 'POST':
            try:
                try:
                    jobID = request.form['jobID']
                    hardware = request.form['edit_job_hardware']
                    start_date = request.form['edit_job_start_date']
                    end_date = request.form['edit_job_end_date']
                    estimated_cost = request.form['edit_estimated_cost']
                    final_cost = request.form['edit_final_cost']
                    charge_amount = request.form['edit_charge_amount']
                    
                    cur.callproc('std_edit_job', (jobID, hardware, start_date, end_date, estimated_cost, final_cost, charge_amount))
                except:
                    hardware = request.form['hardwareName']
                    start_date = request.form['start_date']
                    end_date = request.form['end_date']
                    estimated_cost = request.form['estimated_cost']
                    final_cost = request.form['final_cost']
                    charge_amount = request.form['charge_amount']
                    outID = -1

                    cur.callproc('std_add_job', (hardware, start_date, end_date, estimated_cost, final_cost, charge_amount, outID))
                mysql.connection.commit()
            except:
                flash("Error: Unable to submit new entry, check your database connection")

        if request.method == 'GET':
            search_bar = "search_jobs_bar"#defining searchBar
            if request.args.get(search_bar) != None:#if the argument is in searchbar
                #sqlString = "SELECT * FROM customer_table WHERE name LIKE '%"+ request.args.get("search_customerName") +"%'"
                jobs = cur.execute(select_search(request.args.get(search_bar), 'hardware', 'job_table'))
                connection = True
                if jobs > 0:
                    job_details = cur.fetchall()
                    return render_template('jobs.html', jobDetails = job_details, connected = connection)
        
        jobs = cur.execute("SELECT * FROM job_table")
        connection = True
        if jobs > 0:
            job_details = cur.fetchall()
            return render_template('jobs.html', jobDetails = job_details, connected = connection)
        else:
            return render_template('jobs.html', jobDetails = [], connected = connection)
    except:
        flash("Error: Database unavailable. Not connected to MySQL Database Server")
        return render_template('jobs.html', connected = connection)

@app.route('/order_data', methods = ['GET', 'POST'])
def orders():
    connection = False #validation for sql connection
    try:
        cur = mysql.connection.cursor()
        if request.method == 'POST':
            try:
                ordered_item = request.form['ordered_item']
                est_date = request.form['estimated_delivery_date']
                delivery_date = request.form['delivery_date']
                order_cost = request.form['order_cost']
                outID = -1

                cur.callproc('std_add_order', (ordered_item, est_date, delivery_date, order_cost, outID))
                mysql.connection.commit()
            except:
                flash("Error: Unable to submit new entry, not connected to SQL database")

        if request.method == 'GET':
            search_bar = "search_orders_bar"#defining searchBar
            if request.args.get(search_bar) != None:#if the argument is in searchbar
                orders = cur.execute(select_search(request.args.get(search_bar), 'Ordered_Item', 'orders_table'))
                connection = True
                if orders > 0:
                    order_details = cur.fetchall()
                    return render_template('orders.html', orderDetails = order_details, connected = connection)
        
        orders = cur.execute("SELECT * FROM orders_table")
        connection = True
        if orders > 0:
            order_details = cur.fetchall()
            return render_template('orders.html', orderDetails = order_details, connected = connection)
        else:
            return render_template('orders.html', orderDetails = [], connected = connection)
    except:
        flash("Error: Database unavailable. Not connected to MySQL Database Server")
        return render_template('orders.html', connected = connection)

if __name__ == "__main__":
    app.run(debug = True)

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="5fwja35"
)

print(mydb)