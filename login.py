import os
import urllib.request
from flask_mysqldb import MySQL
from flask import Flask, request, redirect, jsonify,session
from werkzeug.utils import secure_filename
from flask_cors import CORS
from collections import Counter
import re
#from db import mysql
#from werkzeug import check_password_hash
app = Flask(__name__)

app.secret_key = "secret key"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Mks@1997'
app.config['MYSQL_DB'] = 'book'

mysql = MySQL(app)

@app.route('/')
def home():
	if 'username' in session:
		username = session['username']
		return jsonify({'message' : 'You are already logged in', 'username' : username})
	else:
		return jsonify({'message' : 'Unauthorized'})


@app.route('/login', methods=['POST'])
def login():

	cur = mysql.connection.cursor()
	inputdata=request.get_json()
	username = inputdata['username']
	password = inputdata['password']
	query = "SELECT username FROM students WHERE username='"+username+"'"	
	if cur.execute(query, {'username': username}):
		return {"Result":"login successfully"}
	else:
		cur.execute("insert into students (username,password) values ('"+str(username)+"','"+str(password)+"')")
		mysql.connection.commit()
		return {"Result":"redirect to main page"}
	return {"Result":"login successfully"}


@app.route('/logout')
def logout():
	if 'username' in session:
		session.pop('username', None)
	return jsonify({'message' : 'You successfully logged out'})


@app.route('/update',methods=['POST'])
def update():
	cur = mysql.connection.cursor()
	inputdata=request.get_json()
	name = inputdata['name']
	email = inputdata['email']
	username = inputdata['username']

	cur.execute("SELECT username FROM students")
	data = cur.fetchall()
	j = []
	for i in data:
		j.append(i[0])
	if username in j:
		query="UPDATE students SET name='"+str(name)+"', email='"+str(email)+"' WHERE username='"+username+"'"
		cur.execute(query)
		mysql.connection.commit()
		cur.close()
		return {"result":"data updated successfully"}
	else:
		return {"result":"Invalid username"}


@app.route('/update_interest',methods=['POST'])
def update_interest():
	cur = mysql.connection.cursor()
	inputdata=request.get_json()
	interest = inputdata['interest']
	username  = inputdata['username']
	query="UPDATE student_interest SET interest ='"+str(interest)+"' WHERE username='"+username+"'"
	cur.execute(query)
	mysql.connection.commit()
	cur.close()
	return {"result":"Student interest data updated successfully"}


@app.route('/delete', methods = ['DELETE'])
def delete():
    cur = mysql.connection.cursor()
    inputdata = request.get_json()
    username = inputdata['username']
    cur.execute("DELETE FROM student_interest WHERE username='"+username+"'")
    mysql.connection.commit()
    cur.close()
    return {"result":"data deleted successfully"}


@app.route('/distinct')
def distinct():
    cur = mysql.connection.cursor()
    x = cur.execute("select distinct(interest) from student_interest")
    print(x)
    return {"Total distinct interest is ":x}
	

if __name__ == "__main__":
    app.run(debug = True)