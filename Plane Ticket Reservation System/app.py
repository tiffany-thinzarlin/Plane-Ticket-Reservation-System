#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect, jsonify
import pymysql.cursors
import hashlib
import re
from datetime import datetime
import random
import json
#Initialize the app from Flask
app = Flask(__name__)

#################### MISC HELPERS #############################

def hash_helper(password):
	result = hashlib.md5()
	result.update(password.encode())
	return result.hexdigest()

def email_check(email):
	regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
	return re.fullmatch(regex, email)
    


#Configure MySQL
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='root',
                       port = 3306,
                       db='airlines',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)


@app.route('/')
def hello():
	
	flights = view_customer_flight("None", False)
	return render_template('index.html', flights = flights)


#Define route for login
@app.route('/login')
def login():
	return render_template('login.html')

#Define route for register
@app.route('/register')
def register():
	return render_template('register.html')




# verify user
@app.route('/login_customer', methods = ['GET', 'POST'])
def login_customer():
	if request.method == "GET":
		return render_template('login_customer.html', error = None)

	elif request.method == "POST":
	#grabs information from the forms
		email = request.form['email']
		password = request.form['password']
		print(password)

		hashed = hash_helper(password)
		print(hashed)
		#cursor used to send queries
		cursor = conn.cursor()
		#executes query
		
		query = 'SELECT email, cust_password,name  FROM customer WHERE email = %s and cust_password = md5(%s)'
		cursor.execute(query, (email, password))
		#stores the results in a variable, #use fetchall() if you are expecting more than 1 data row
			
		data = cursor.fetchone()
		cursor.close()
		error = None

		if(data):
			#creates a session for the the user
			#session is a built in
			session['email'] = email
			session['role'] = "customer"
			session['loggedin'] = True
			session['name']=data['name']
			return redirect(url_for('customer_home'))
		else:
			#returns an error message to the html page
			error = 'Invalid login!'
			return render_template('login_customer.html', error=error)


@app.route('/login_staff', methods=['GET', 'POST'])
def login_staff():
	if request.method == "GET":
		return render_template('login_staff.html', error = None)
	elif request.method == "POST":
	#grabs information from the forms
		username = request.form['username']
		password = request.form['password']
		print(password)

		hashed = hash_helper(password)
		print(hashed)
		#cursor used to send queries
		cursor = conn.cursor()
		#executes query
		
		query = 'SELECT user_name, password, airline_name FROM airline_staff WHERE user_name = %s and password = md5(%s)'
		cursor.execute(query, (username, password))
		#stores the results in a variable, #use fetchall() if you are expecting more than 1 data row
			
		data = cursor.fetchone()
		cursor.close()
		error = None

		if(data):
			#creates a session for the the user
			#session is a built in
			airline = data['airline_name']
			session['username'] = username
			session['role'] = "staff"
			session['airline'] = airline
			session["loggedin"] = True
			return redirect(url_for('staff_home'))
		else:
			#returns an error message to the html page
			error = 'Invalid login!'
			return render_template('login_staff.html', error=error)


@app.route('/register_customer', methods=['GET', 'POST'])
def register_customer():
	if request.method == "POST":
	#grabs information from the forms
		email = request.form['email']
		password = request.form['password']
		name = request.form['Your Name']
		building_num = request.form['Building Number']
		address = request.form['Address']
		city = request.form['City']
		state = request.form['State']
		phone= request.form['Phone Number']
		passport_num = request.form['Passport Number']
		passport_exp = request.form['Passport Expiration Date']	
		country = request.form['Passport Country']
		dob = request.form['Birthday']


		if email_check(email):				# Check for valid email format
			query = 'SELECT * FROM customer WHERE email = %s'
			#cursor used to send queries
			cursor = conn.cursor()
			cursor.execute(query, (email))
			data = cursor.fetchone()          #use fetchall() if you are expecting more than 1 data row
			error = None

			if(data):
			#If the previous query returns data, then user exists
				error = "This user already exists"
				return render_template('register_customer.html', error = error)
			else:
				ins = 'INSERT INTO customer (name, email, cust_password, building_num, street, city, state, cust_phone_num, passport_num, passport_expiration, passport_country,cust_dob ) VALUES(%s, %s,md5(%s),%s,%s,%s,%s,%s,%s,%s,%s,%s)'
				hashed = hash_helper(password)
				cursor.execute(ins, (name, email,password, building_num, address, city, state, phone, passport_num, passport_exp,country,dob))
				conn.commit()
				cursor.close()
				return render_template('index.html')
		else:
			error = "Invalid Email!"
			return render_template('register_customer.html', error = error)
			
	elif request.method == "GET":
		return render_template('register_customer.html', error = None)


@app.route('/register_staff', methods=['GET', 'POST'])
def register_staff():
	if request.method == "POST":
		#grabs information from the forms
		username = request.form['username']
		password = request.form['password']
		airline = request.form['Airline']
		first_name = request.form['First Name']
		last_name = request.form['Last Name']
		dob = request.form['Date of Birth']
		phone = request.form['Phone Number']
		query = 'SELECT * FROM airline_staff WHERE user_name = %s'
		phone_query = 'SELECT * FROM staff_phone WHERE user_name = %s'

		#cursor used to send queries
		cursor = conn.cursor()
		cursor.execute(query, (username))
		data = cursor.fetchone()				#use fetchall() if you are expecting more than 1 data row

		cursor.execute(phone_query, (username))
		phone_data = cursor.fetchone()
		
		error = None

		if(data) and (phone_data):
		#If the previous query returns data, then user exists
			error = "This user already exists"
			return render_template('register_staff.html', error = error)
		else:
			ins = 'INSERT INTO airline_staff VALUES(%s, %s, %s, %s, md5(%s), %s)'
			phone_que = 'INSERT INTO staff_phone VALUES(%s, %s)'
			hashed = hash_helper(password)
			cursor.execute(ins, (airline, username,first_name, last_name, password, dob))
			print(phone)
			conn.commit()
			cursor.execute(phone_que, (username, phone))
			conn.commit()
			cursor.close()
			return render_template('index.html')
	else:
		return render_template("register_staff.html", error = None)


	
@app.route('/logout')
def logout():
	if session["role"] == "customer":
		session.pop('email')
	else:
		session.pop('username')

	return redirect('/')
	
	


###################STAFF CORNER###################################

@app.route('/staff_home', methods=['POST', 'GET'])
def staff_home():
	if request.method == "GET":
		if session["loggedin"] and session["role"] == "staff" and "username" in session :
			username = session["username"]
			flights = view_staff_flight(username)
			return render_template("staff_home.html", flights = flights, show_button = True, username = username)
		else:
			return render_template("error.html", error="User not logged in")


@app.route("/staff_flights", methods=["GET"])
def staff_flights():
	if session["loggedin"] and session["role"] == "staff" and "username" in session:  # verify customer
		# view flights
		airline_name = session["airline"]
		flights = view_staff_flight(airline_name)  # default use case, view future flights
		# print(flights)
		return render_template("staff_home.html", flights=flights, show_button=False)
	else:
		return render_template("error.html", error="User not logged in")


@app.route("/search_flight_staff", methods=['GET', 'POST'])
def search_flight_staff():
	if session['loggedin'] and session['role'] == "staff" and "username" in session:
		if request.method == 'POST' :
			dept_airport = request.form['depart']
			arr_airport = request.form['arrive']
			start = request.form['start time']
			datetime.strptime(start, '%Y-%m-%dT%H:%M')
			end = request.form['end time']
			datetime.strptime(end, '%Y-%m-%dT%H:%M')
			airline = session["airline"]


			query = 'SELECT * FROM flight WHERE flight.airline_name = %s AND flight.departure_airport_code = %s AND flight.arrival_airport_code = %s AND (flight.departure_date_time BETWEEN %s AND %s)'

			cursor = conn.cursor()
			cursor.execute(query, (airline, dept_airport, arr_airport, start, end))
			data = cursor.fetchall()
			if (data):
				return render_template("search_flight_staff.html", show = True, flights = data, error=None)
			else:
				error = "could not find any flight. Try again"
				return render_template("search_flight_staff.html", show = False, flights = None, serror=error)
		else: return render_template("search_flight_staff.html", show = False, error=None)

	else: return render_template("error.html", error="User not logged in")


@app.route('/create_new_flights')
def create_new_flights():
	if session['loggedin'] and session['role'] == "staff" and "username" in session:
		username = session['username']
		cursor = conn.cursor()
		query = 'SELECT flight.airplane_ID, flight.airline_name, flight.flight_num, flight.base_price, flight.status, flight.departure_date_time, flight.arrival_date_time, flight.departure_airport_code, flight.arrival_airport_code FROM flight, airline_staff WHERE airline_staff.airline_name = flight.airline_name AND airline_staff.user_name = %s AND (flight.departure_date_time BETWEEN CURDATE() AND DATE_ADD(CURDATE(),INTERVAL 30 DAY))'
		cursor.execute(query, (username))
		data = cursor.fetchall()
		cursor.close()
		return render_template('create_new_flights.html', posts = data)
	else: return render_template("error.html", error="User not logged in")

@app.route('/create_new_flights_post',methods=['GET', 'POST'])
def create_new_flights_post():
	if session['loggedin'] and session['role'] == "staff" and "username" in session:
		cursor = conn.cursor()
		airplane_ID = request.form['airplane_ID']
		airline_name = request.form['airline_name']
		flight_num = request.form['flight_num']
		base_price = request.form['base_price']
		status = request.form['status']
		departure_date_time = request.form['departure_date_time']
		arrival_date_time = request.form['arrival_date_time']
		departure_airport_code = request.form['departure_airport_code']
		arrival_airport_code = request.form['arrival_airport_code']

		query = 'INSERT INTO flight(airplane_ID, airline_name, flight_num, base_price, status, departure_date_time, arrival_date_time, departure_airport_code, arrival_airport_code) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
		cursor.execute(query, (airplane_ID, airline_name, flight_num, base_price, status, departure_date_time, arrival_date_time, departure_airport_code, arrival_airport_code))
		conn.commit()
		cursor.close()
		return redirect(url_for('create_new_flights'))
	else: return render_template("error.html", error="User not logged in")


@app.route('/add_airplane')
def add_airplane():
	if session['loggedin'] and session['role'] == "staff" and "username" in session:
		username = session['username']
		cursor = conn.cursor()
		query = 'SELECT airplane.airline_name, airplane.airplane_ID, airplane.num_of_seats FROM airline_staff, airplane WHERE airline_staff.user_name = %s AND airline_staff.airline_name = airplane.airline_name'
		cursor.execute(query, (username))
		data1 = cursor.fetchall()
		cursor.close()
		return render_template('add_airplane.html', username = username, posts=data1)
	else: return render_template("error.html", error="User not logged in")

@app.route('/post', methods=['GET', 'POST'])
def post():
	if session['loggedin'] and session['role'] == "staff" and "username" in session:
		username = session['username']
		cursor1 = conn.cursor()
		query1 = 'SELECT airline_name FROM airline_staff WHERE airline_staff.user_name = %s'
		cursor1.execute(query1, (username))
		airline_name = cursor1.fetchone()
		airline_name = airline_name.get('airline_name')
		airplane_ID = request.form['airplane_ID']
		num_of_seats = request.form['num_of_seats']
		query = 'INSERT INTO airplane (airline_name, airplane_ID, num_of_seats) VALUES (%s, %s, %s)'
		cursor1.execute(query, (airline_name, airplane_ID, num_of_seats))
		conn.commit()
		cursor1.close()
		return redirect(url_for('add_airplane'))
	else: return render_template("error.html", error="User not logged in")

@app.route('/add_airport')
def add_airport():
	if session['loggedin'] and session['role'] == "staff" and "username" in session:
		cursor = conn.cursor();
		query = 'SELECT airport_code, airport_name, airport_city FROM airport'
		cursor.execute(query)
		data = cursor.fetchall()
		cursor.close()
		return render_template('add_airport.html', posts = data)
	else: return render_template("error.html", error="User not logged in")

@app.route('/add_airport_post', methods=['GET', 'POST'])
def add_airport_post():
	if session['loggedin'] and session['role'] == "staff" and "username" in session:
		cursor = conn.cursor()
		airport_code = request.form['airport_code']
		airport_name = request.form['airport_name']
		airport_city = request.form['airport_city']
		query = 'INSERT INTO airport(airport_code, airport_name, airport_city) VALUES (%s, %s, %s)'
		cursor.execute(query, (airport_code, airport_name, airport_city))
		conn.commit()
		cursor.close()
		return redirect(url_for('add_airport'))
	else: return render_template("error.html", error="User not logged in")

@app.route('/change_status', methods = ['GET', 'POST'])
def change_status():
	if request.method == "POST":
		if session['loggedin'] and session['role'] == "staff" and "username" in session:
			username = session['username']
			cursor = conn.cursor()
			flight_num = request.form['flight_num']
			departure_date_time = request.form['departure_date_time']
			datetime.strptime(departure_date_time, '%Y-%m-%dT%H:%M')
			status = request.form['status']
			query = 'SELECT * FROM flight, airline_staff WHERE flight.flight_num = %s AND flight.departure_date_time = %s AND airline_staff.user_name = %s AND airline_staff.airline_name = flight.airline_name'
			cursor.execute(query, (flight_num, departure_date_time, username))
			data = cursor.fetchone()
			if (data):
				query1 = 'UPDATE flight SET status = %s WHERE flight_num = %s AND departure_date_time = %s'
				cursor.execute(query1, (status, flight_num, departure_date_time))
				conn.commit()
				cursor.close()
				#return render_template('change_status.html', error = "Status has changed!")
				return redirect(url_for('staff_home'))
			else:
				cursor.close()
				error = "This flight does not exist"
				return render_template('change_status.html', error = error)
		else: return render_template("error.html", error="User not logged in")
	elif request.method == "GET":
		return render_template('change_status.html', error = None)

@app.route('/view_flight_ratings')
def view_flight_ratings():
	if session['loggedin'] and session['role'] == "staff" and "username" in session:
		username = session['username']
		cursor = conn.cursor()
		query = 'SELECT rate.flight_num, rate.email, rate.rating, rate.comment FROM airline_staff, flight, rate WHERE airline_staff.user_name= %s AND flight.airline_name = airline_staff.airline_name AND flight.flight_num = rate.flight_num order by rate.flight_num'
		cursor.execute(query,(username))
		data = cursor.fetchall()
		cursor.close()
		return render_template('view_flight_ratings.html', posts=data)
	else: return render_template("error.html", error="User not logged in")

@app.route('/view_avg_flight_ratings')
def view_avg_flight_ratings():
	if session['loggedin'] and session['role'] == "staff" and "username" in session:
		username = session['username']
		cursor = conn.cursor()
		query = 'SELECT rate.flight_num, avg(rate.rating) FROM airline_staff, flight, rate WHERE airline_staff.user_name= %s AND flight.airline_name = airline_staff.airline_name AND flight.flight_num = rate.flight_num group by flight.flight_num'
		cursor.execute(query, (username))
		data = cursor.fetchall()
		cursor.close()
		return render_template('view_avg_flight_ratings.html', posts=data)
	else: return render_template("error.html", error="User not logged in")


@app.route('/view_frequent_customers')
def view_frequent_customers():
	if session['loggedin'] and session['role'] == "staff" and "username" in session:
		username = session['username']
		cursor = conn.cursor()
		#query =  'SELECT  distinct customer.name, customer.email FROM ticket, airline_staff, customer WHERE airline_staff.user_name = %s AND ticket.airline_name = airline_staff.airline_name AND ticket.email = customer.email AND ticket.departure_date_time BETWEEN DATE_ADD(CURDATE(),INTERVAL -1 year) AND CURDATE() ORDER BY (SELECT count(*) FROM ticket, airline_staff, customer WHERE airline_staff.user_name = %s AND ticket.airline_name = airline_staff.airline_name AND ticket.email = customer.email AND ticket.departure_date_time BETWEEN DATE_ADD(CURDATE(),INTERVAL -1 year) AND CURDATE()) '
		query = 'SELECT customer.name, customer.email FROM ticket, airline_staff, customer WHERE airline_staff.user_name = %s AND ticket.airline_name = airline_staff.airline_name AND ticket.email = customer.email AND ticket.departure_date_time BETWEEN DATE_ADD(CURDATE(),INTERVAL -1 year) AND CURDATE() GROUP BY customer.email ORDER BY (count(customer.name)) DESC '
		cursor.execute(query, username)
		data = cursor.fetchall()
		cursor.close()
		return render_template('view_frequent_customers.html', posts=data)
	else: return render_template("error.html", error="User not logged in")



#
@app.route('/view_report', methods=['GET', 'POST'])
def view_report():
	if request.method =='GET':
		return render_template('report.html', data=None, error=None, month=0)
	else:
		if session['loggedin'] and session['role'] == "staff" and "username" in session:
			airline = session['airline']
			start_date = request.form['start_date']
			end_date = request.form['end_date']

			data = get_ticket_count(airline, start_date, end_date)
			if data:
				
				return render_template('report.html', data=data, error=None, month=len(data))
			else:
				error = "Did not retrieve any data, try again!"
				return render_template('report.html', data=None, error=error, month=0)
		else: return render_template("error.html", error="User not logged in")


@app.route('/view_earned_revenue')
def view_earned_revenue():
	if session['loggedin'] and session['role'] == "staff" and "username" in session:
		username = session['username']
		cursor = conn.cursor()
		query = 'SELECT sum(ticket.sold_price) FROM ticket, airline_staff WHERE airline_staff.user_name = %s AND airline_staff.airline_name = ticket.airline_name AND ticket.purchase_date_time BETWEEN DATE_ADD(CURDATE(),INTERVAL -1 year) AND CURDATE() group by airline_staff.airline_name'
		query1 = 'SELECT sum(ticket.sold_price) FROM ticket, airline_staff WHERE airline_staff.user_name = %s AND airline_staff.airline_name = ticket.airline_name AND ticket.purchase_date_time BETWEEN DATE_ADD(CURDATE(),INTERVAL -3 month) AND CURDATE() group by airline_staff.airline_name'
		cursor.execute(query, (username))
		data = cursor.fetchone()
		cursor.execute(query1, username)
		data1 = cursor.fetchone()
		cursor.close()

		return render_template('view_earned_revenue.html', posts = data, threemonths = data1)
	else: return render_template("error.html", error="User not logged in")

	
	

@app.route('/view_top_destinations')
def view_top_destinations():
	if session['loggedin'] and session['role'] == "staff" and "username" in session:
		username = session['username']
		cursor = conn.cursor()
		query = 'SELECT airport.airport_city FROM airline_staff, ticket, flight, airport WHERE airline_staff.user_name = %s AND airline_staff.airline_name = ticket.airline_name AND flight.flight_num = ticket.flight_num AND flight.arrival_airport_code = airport.airport_code AND (flight.arrival_date_time BETWEEN DATE_ADD(CURDATE(),INTERVAL -3 month) AND CURDATE())GROUP BY airport.airport_city ORDER BY (count(airport.airport_city)) DESC LIMIT 3'
		query1 = 'SELECT airport.airport_city FROM airline_staff, ticket, flight, airport WHERE airline_staff.user_name = %s AND airline_staff.airline_name = ticket.airline_name AND flight.flight_num = ticket.flight_num AND flight.arrival_airport_code = airport.airport_code AND (flight.arrival_date_time BETWEEN DATE_ADD(CURDATE(),INTERVAL -1 year) AND CURDATE())GROUP BY airport.airport_city ORDER BY (count(airport.airport_city)) DESC LIMIT 3'
		cursor.execute(query, username)
		data = cursor.fetchall()
		print(data)
		cursor.execute(query1, username)
		data1 = cursor.fetchall()
		print(data1)
		cursor.close()
		return render_template('view_top_destinations.html', posts = data, oneyear = data1)
	else: return render_template("error.html", error="User not logged in")


@app.route('/view_customer_in_flight', methods=['POST', 'GET'])
def view_customer_in_flight():
	if session['loggedin'] and session['role'] == "staff" and "username" in session:
		if request.method == "POST":
			airline_name = session['airline']
			flight_num = request.form['flight_num']
			departure_date_time = request.form['departure_date_time']
			datetime.strptime(departure_date_time, '%Y-%m-%dT%H:%M')
			cursor = conn.cursor()
			query = 'SELECT distinct customer.name, customer.email FROM ticket,flight,customer WHERE flight.airline_name = %s AND flight.flight_num = %s AND flight.flight_num = ticket.flight_num AND flight.departure_date_time = ticket.departure_date_time AND flight.departure_date_time = %s AND ticket.email = customer.email '
			cursor.execute(query,(airline_name, flight_num, departure_date_time))
			data = cursor.fetchall()
			cursor.close()
			print("here")
			print(data)
			return render_template('view_customer_in_flight.html', posts = data, show = True)

		else:
			return render_template('view_customer_in_flight.html', posts = None, show = False)
	else: return render_template("error.html", error="User not logged in")






############################################################################# CUSTOMER CORNER ###################################################################################
@app.route('/customer_home', methods=['POST', 'GET'])
def customer_home():
	# request.args()
	if request.method == "GET":
		if session["loggedin"] and session["role"] == "customer" and "email" in session:  # verify customer
			# view flights
			email = session["email"]
			name = session['name']
			flights = view_customer_flight(email, False)  # default use case, view future flight
			ratings = fetch_ratings(email)
			return render_template("customer_home.html", name=name, flights=flights, show_button=True, ratings=ratings)
		else:
			return render_template("error.html", error="User not logged in")


@app.route("/customer_flights", methods=["GET"])
def customer_flights():  # view customer flights, using the same customer_home page
	if session["loggedin"] and session["role"] == "customer" and "email" in session:  # verify customer
		# view flights
		flights = view_customer_flight(session["email"], True)  # view purchased flight
		# print(flights)
		return render_template("customer_home.html", flights=flights, show_button=False, ratings=None)
	else:
		return render_template("error.hmtl", error="User not logged in")


@app.route("/search_flight", methods=['GET', 'POST'])
def search_flight():
	if session["loggedin"]:  # check if logged in to go back to cust home or to index
		cust_home = True
	else:
		cust_home = False

	# print(cust_home)

	if request.method == "POST":
		if session["loggedin"] and session["role"] == "customer" and "email" in session:  # verify customer
			depart_airport = request.form["depart"]
			arrive_airport = request.form["arrive"]
			depart_date = request.form["departure date"]
			return_date = request.form["return date"]
			way = request.form["way"]
			cursor = conn.cursor()

			if way == "one way":
				query = "SELECT flight.airplane_ID, flight.airline_name, flight.flight_num,flight.base_price,flight.status FROM flight WHERE %s = SUBSTRING(departure_date_time,1,10) AND %s = departure_airport_code AND %s = arrival_airport_code"
				cursor.execute(query, (depart_date, depart_airport, arrive_airport))
				flights = cursor.fetchall()
				print(flights)

			elif way == "return":
				query = "SELECT flight.airplane_ID, flight.airline_name, flight.flight_num,flight.base_price,flight.status FROM flight WHERE %s = SUBSTRING(departure_date_time,1,10) AND %s = departure_airport_code AND %s = arrival_airport_code"
				query2 = "SELECT flight.airplane_ID, flight.airline_name, flight.flight_num,flight.base_price,flight.status FROM flight WHERE %s = SUBSTRING(departure_date_time,1,10) AND %s = departure_airport_code AND %s = arrival_airport_code"

				cursor.execute(query, (depart_date, depart_airport, arrive_airport))
				flights = cursor.fetchall()

				cursor.execute(query2, (return_date, arrive_airport, depart_airport))
				flight2 = cursor.fetchall()

				for item in flight2:
					flights.append(item)
				print(flights)

			if flights:
				show = True
			else:
				show = False

			return render_template("search_flight.html", show=show, flights=flights, cust_home=cust_home)
		else:
			return render_template("error.hmtl", error="User not logged in")
	else:
		return render_template("search_flight.html", show=False, flights=None, cust_home=cust_home)


@app.route('/purchase_ticket', methods=['GET', 'POST'])
def purchase_ticket():
	if request.method == "GET":
		return render_template("purchase.html", error=None)
	else:
		if session["loggedin"] and session["role"] == "customer" and "email" in session:
			# validate flight existence
			flight_num = request.form['flight number']
			date_time = request.form['date time']
			card_type = request.form['card type']
			card_num = request.form['card number']
			name_card = request.form['name on card']
			exp_date = request.form['expiration date']
			email = session['email']

			date_time = date_time.replace("T", " ")  # get right format of date

			print(flight_num, date_time)

			flight_q = 'SELECT * FROM flight WHERE %s = flight_num AND %s = SUBSTRING(departure_date_time,1,16)'  # used substring to filter seconds
			cursor = conn.cursor()
			cursor.execute(flight_q, (flight_num, date_time))
			flight = cursor.fetchone()
			print(flight)

			if not flight:
				error = "Flight does not exist! Please check your information"
				return render_template("purchase.html", error=error)
			else:
				# print(flight)
				price = flight['base_price']
				de_time = flight['departure_date_time']
				airline = flight['airline_name']
				plane_id = flight["airplane_ID"]

				# get number of seats from the airplane to adjust price
				total_seat_q = "SELECT num_of_seats FROM airplane WHERE %s = airplane_ID"
				cursor.execute(total_seat_q, (plane_id))
				total_seat = int(cursor.fetchone()['num_of_seats'])  # capacity of plane
				print(total_seat)

				count_q = "SELECT COUNT(*) as count FROM ticket WHERE %s = flight_num"
				cursor.execute(count_q, (flight_num))
				seat_num = int(cursor.fetchone()['count'])  # number of seat purchased on plane

				if seat_num >= 0.75 * total_seat:  # increase by 20 percent if condition met
					price = int(price) * 1.20

				ticket_q = 'INSERT INTO ticket (email, airplane_ID, airline_name, flight_num, departure_date_time, sold_price, card_type, card_num, name_on_card, expiration_date,purchase_date_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW())'
				cursor.execute(ticket_q, (
				email, plane_id, airline, flight_num, de_time, price, card_type, card_num, name_card, exp_date))
				conn.commit()

				# GET THE TICKET ID FROM TICKET JUST CREATED, USE THAT TO CREATE TICKET FOR PURCHASES
				id_q = 'SELECT ticket_ID FROM ticket ORDER BY purchase_date_time DESC LIMIT 0,1'
				cursor.execute(id_q)
				data = cursor.fetchone()
				print("curr_data:", data)
				ticket_id = data['ticket_ID']

				purchase_q = 'INSERT INTO purchase VALUES(%s,%s)'
				cursor.execute(purchase_q, (ticket_id, email))
				conn.commit()

				cursor.close()
				return redirect(url_for('customer_home'))
		else:
			return render_template("error.html")


@app.route('/rate', methods=['GET', 'POST'])
def rate():
	if request.method == "GET":
		return render_template("rate.html", error=None)
	else:
		if session["loggedin"] and session["role"] == "customer" and "email" in session:
			# retrieve data from html form
			email = session['email']
			flight_num = request.form['flight number']
			ticket_id = request.form['ticketid']
			rating = request.form['rating']
			comment = request.form['comment']

			# validate whether customer bought the ticket and the date in the past
			query = 'SELECT * FROM ticket WHERE %s = email AND %s = flight_num AND %s = ticket_ID AND purchase_date_time <= CURRENT_TIMESTAMP()'
			cursor = conn.cursor()
			cursor.execute(query, (email, flight_num, ticket_id,))
			data = cursor.fetchone()
			print("HERE", data)

			if (data):  # found a flight
				insert_q = 'INSERT INTO rate VALUES (%s, %s, %s, %s)'
				cursor.execute(insert_q, (flight_num, email, rating, comment))
				conn.commit()
				cursor.close()
				return redirect(url_for('customer_home'))
			else:
				error = "Flight not found, please check your information and try again!"
				return render_template("rate.html", error=error)
		else:
			return render_template("error.html")


@app.route('/trackmyspending', methods=['GET', 'POST'])
def spending():
	if request.method == 'GET':
		# default value - 6 months
		if session["loggedin"] and session["role"] == "customer" and "email" in session:
			spending = get_spending(session['email'])
			print(spending)

			total = 0
			for item in spending:
				total += item['month_total']

			return render_template('spending.html', spending=spending, error=False, total=total, month_num=6)
	else:
		if session["loggedin"] and session["role"] == "customer" and "email" in session:
			email = session['email']
			start_month = request.form['start month']
			end_month = request.form['end month']
			print(start_month)
			print(end_month)

			spending = get_spending(email, start_month, end_month)

			if spending:
				print("in post", spending)
				total = 0
				month_num = 0
				for item in spending:
					total += item['month_total']
					month_num += 1
				return render_template("spending.html", spending=spending, error=None, total=total, month_num=month_num)
			else:
				error = "Something went wrong! Please check your month range and try again"
				return render_template("spending.html", spending=None, error=error)
		else:
			return render_template("error.html")


####################### MISC HELPER ###############################################################################################################################################


def view_customer_flight(email, purchased=False):
	# home function will already have customer personal details (email, pass, etc)
	cursor = conn.cursor()
	if purchased:
		query = 'SELECT ticket.ticket_ID, flight.airplane_ID, flight.airline_name, flight.flight_num, ticket.sold_price, flight.status, flight.departure_date_time, flight.arrival_date_time, flight.departure_airport_code, flight.arrival_airport_code FROM flight, purchase, customer, ticket WHERE purchase.email = %s AND customer.email = purchase.email AND ticket.flight_num = flight.flight_num AND ticket.ticket_ID = purchase.ticket_ID'
		cursor.execute(query, (email))
	else:  # default: view future flights
		query = 'SELECT * FROM flight WHERE departure_date_time > CURDATE()'
		cursor.execute(query)

	data = cursor.fetchall()
	print(data)
	return data


def view_staff_flight(username):
	# staff view flight needs airline that staff works in as arg
	cursor = conn.cursor()
	query = 'SELECT flight.airplane_ID, flight.airline_name, flight.flight_num, flight.base_price, flight.status, flight.departure_date_time, flight.arrival_date_time, flight.departure_airport_code, flight.arrival_airport_code FROM flight, airline_staff WHERE flight.airline_name = airline_staff.airline_name AND airline_staff.user_name = %s AND (departure_date_time BETWEEN CURDATE() AND DATE_ADD(CURDATE(),INTERVAL 30 DAY))'
	cursor.execute(query, (username))
	data = cursor.fetchall()
	print(data)
	return data


def fetch_ratings(email):
	query = 'SELECT flight_num, rating, comment FROM rate WHERE email = %s'
	cursor = conn.cursor()
	cursor.execute(query, (email))
	ratings = cursor.fetchall()
	cursor.close()
	return ratings


def get_spending(email, start_month=None, end_month=None):
	cursor = conn.cursor()
	if not start_month and not end_month:
		query = "SELECT MONTHNAME(purchase_date_time) as month, SUM(sold_price) as month_total FROM ticket WHERE email=%s AND MONTH(CURDATE()) - 6 GROUP BY YEAR(purchase_date_time), MONTH(purchase_date_time)"
		cursor.execute(query, (email))
	else:
		query = "SELECT MONTHNAME(purchase_date_time) as month, SUM(sold_price) as month_total FROM ticket WHERE email=%s AND DAY(%s)<=DAY(purchase_date_time) AND DAY(%s)>=DAY(purchase_date_time) AND MONTH(%s)<=MONTH(purchase_date_time) AND MONTH(%s)>=MONTH(purchase_date_time) AND YEAR(%s)<=YEAR(purchase_date_time) AND YEAR(%s)>=YEAR(purchase_date_time) GROUP BY YEAR(purchase_date_time), MONTH(purchase_date_time);"
		print("HELLEO")
		cursor.execute(query, (email, start_month, end_month, start_month, end_month, start_month, end_month))

	data = cursor.fetchall()
	print("SPENDING: ", data)
	return data

def get_ticket_count(airline, start_month, end_month):
	cursor = conn.cursor()
	query = 'SELECT MONTHNAME(purchase_date_time) as month, COUNT(ticket_ID) as tick_total FROM ticket WHERE airline_name=%s AND purchase_date_time between %s and %s GROUP BY YEAR(purchase_date_time), MONTH(purchase_date_time);'
	cursor.execute(query,(airline,start_month,end_month))
	data = cursor.fetchall()
	print("TICKET COUNT: ", data)
	return data

def hash_helper(password):
	result = hashlib.md5()
	result.update(password.encode())
	return result.hexdigest()


def email_check(email):
	regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
	return re.fullmatch(regex, email)


app.secret_key = 'some key that you will never guess'
if __name__ == "__main__":
	app.run('127.0.0.1', 6500, debug=True)

