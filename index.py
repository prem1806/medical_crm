import os
import requests
import json
import simplejson as json
import sqlite3
from flask import Flask, jsonify, request, session, redirect, url_for, abort, render_template, flash

app = Flask(__name__)
DATABASE = "medicine.db"

#data base connection.... 

def connect_db():
    conn = sqlite3.connect(DATABASE)
    return conn    

#insert_data_to_db for add table

def insert_data_to_db(name, quantity, cp, sp):
    query = "insert into medicine_details (name, quantity, cost_price, selling_price) \
             values ('%s', %d, %f, %f)" %(name, quantity, cp, sp)
    conn = connect_db()
    conn.execute(query)
    conn.commit()
    conn.close()


#insert_data_to_db for signup 
def insert_data_to_db(user_name,password):
    print user_name, password
    query = "insert into user_signup (name,password) values('%s','%s')" %(user_name,password)
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    conn.close()



#chech_in_medicine_db for selling medicine...
def check_in_medicine_db(name, quantity):
    query = "select * from medicine_details where name = '%s' limit 1" %(name)
    conn = connect_db()
    cursor = conn.execute(query)
    results = cursor.fetchall()
    if not results:
        return 0.0
    else:
        row = results[0]
        row = list(row)
        sp  = int(row[3])
        return quantity * sp


# check_in_db for login...        

def check_in_db(user_name,password):
    query = "select * from user_details where uname = '%s' and password = '%s'" %(user_name,password)
    conn = connect_db()
    cursor = conn.execute(query)


def check_in_db(user_name,password):
    print "i am here"
    print "i am good"
    query ="select * from user_signup where name ='%s' and password = '%s'" %(user_name,password)
    print query
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    if not results:
        return 0
    else:
        return render_template('sell_medicine.html')
    

#login 
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/send_login_data', methods=['GET', 'POST'])
def send_login_data():
    user_name = request.form['uname']
    password = request.form['password']
    print "in login:"
    print user_name, password
    if check_in_db(user_name,password):
        return render_template('sell_medicine.html')
    else:
        return render_template('login.html')



# signup 
@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/send_signup_data', methods=['GET', 'POST'])
def send_signup_data():
    user_name = request.form['uname']
    password = request.form['password']
    mail = request.form['mail']
    print user_name, password
    insert_data_to_db(user_name, password)
    return render_template('login.html')



#add medicine
@app.route('/')
def add_medicine():
    return render_template('add_medicine.html')

@app.route('/show_data', methods=['GET', 'POST'])
def show_data():
    medicine_name = request.form['mname']
    medicine_quantity = int(request.form['quantity'])
    medicine_cp = float(request.form['cp'])
    medicine_sp = float(request.form['sp'])
    insert_data_to_db(medicine_name, medicine_quantity, medicine_cp, medicine_sp)
    return render_template('add_medicine.html')


#sell medicine

@app.route('/sell_medicine')
def sell_medicine():
    return render_template('sell_medicine.html')

@app.route('/send_medicine_data',methods=['GET','POST'])
def send_medicine_data():
    medicine_name = request.form['mname']
    medicine_quantity = int(request.form['quantity'])
    total_price = check_in_medicine_db(medicine_name, medicine_quantity)
    if total_price > 0:
        return render_template('show_price.html', total_price=total_price, medicine_name=medicine_name)
    else:
        return render_template('error.html', medicine_name=medicine_name)




if __name__ == "__main__":
	app.run()

