from flask import Flask, render_template, request, redirect
import sqlite3
from sqlite3 import Error

app = Flask(__name__)
DATABASE = "C:/Users/d.benseman/OneDrive - Wellington College/13DTS/Python2022/13-3/Smile/smile.db"


def create_connection(db_file):
    """
    Create a connection with the database
    parameter: name of the database file
    returns: a connection to the file
    """
    print(db_file)
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)
    return None


@app.route('/')
def render_homepage():
    return render_template('home.html')


@app.route('/menu')
def render_menu_page():
    con = create_connection(DATABASE)

    query = "SELECT name, description, volume, price, image FROM product"
    cur = con.cursor()     # Creates a cursor to write the query
    cur.execute(query)     # Runs the query
    product_list = cur.fetchall()
    print(product_list)
    con.close()

    return render_template('menu.html', products=product_list)


@app.route('/contact')
def render_contact_page():
    return render_template('contact.html')


@app.route('/login', methods=['GET', 'POST'])
def render_login_page():
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def render_signup_page():
    if request.method == 'POST':
        print(request.form)
        fname = request.form.get('fname').title().strip()
        lname = request.form.get('lname').title().strip()
        email = request.form.get('email').lower().strip()
        password = request.form.get('password')
        password2 = request.form.get('password2')

        # Check to see whether the passwords match
        if password != password2:
            return redirect('/signup?error=Passwords+do+not+match')

        if len(password) < 8:
            return redirect('/signup?error=Password+must+be+at+least+8+characters')

        con = create_connection(DATABASE)

        query = "INSERT INTO customer (fname, lname, email, password) VALUES (?, ?, ?, ?)"

        cur = con.cursor()
        cur.execute(query, (fname, lname, email, password))
        con.commit()
        con.close()
        return redirect('/login')

    return render_template('signup.html')


app.run(host='127.0.0.1', debug=True)
