import sqlite3
import pandas as pd
import json
from hashlib import sha256

db = "database.db"

def create_user(name, email, password):
	conn = sqlite3.connect(db)

	# check for valid new username and EMAIL
	query = "SELECT NAME FROM users WHERE NAME = \"{}\"".format(name)
	df = pd.read_sql_query(query, conn)
	if len(df) > 0:
		conn.close()
		return "username already taken"

	query = "SELECT NAME FROM users WHERE EMAIL = \"{}\"".format(email)
	df = pd.read_sql_query(query, conn)
	if len(df) > 0:
		conn.close()
		return "email already taken"

	print(query)
	print(df)
	# get unique user id
	query = "SELECT * FROM users;"
	df = pd.read_sql_query(query, conn)
	ID = len(df)

	# hash password
	password = sha256(password.encode('utf-8')).hexdigest()

	c = conn.cursor()
	contacts =  '{"contacts":[]}'
	messages = '{"messages":[]}'
	c.execute("INSERT INTO users VALUES (\'{}\', \'{}\',\'{}\',\'{}\',\'{}\',\'{}\');".format(ID, email, name, password, contacts, messages))
	print("inserted user")
	conn.commit()
	conn.close()

	return "registration successful!"


def check_user(user, password):
	conn = sqlite3.connect(db)

	# check for valid new username and EMAIL
	query = "SELECT * FROM users WHERE NAME = \"{}\"".format(user)
	df = pd.read_sql_query(query, conn)

	# no users found
	if len(df) == 0:
		return -1

	password = sha256(password.encode('utf-8')).hexdigest()

	db_pass = df["PASSWORD"].to_list()[0]

	print(password)
	print(db_pass)

	if db_pass == password:
		print('password correct')
		print(df["PASSWORD"])
		return 1
	else:
		print('password incorrect')
		return 0

def list_users(search=None):
	# allows to search for users or list every user on the platform
	conn = sqlite3.connect(db)

	# no search
	if search == None:
		query = "SELECT NAME FROM users"
		df = pd.read_sql_query(query, conn)
		return df["NAME"].values
	else:
		query = "SELECT * FROM users WHERE NAME = \"{}\"".format(search)
		df = pd.read_sql_query(query, conn)
		return df["NAME"].values



def add_contact(user, contact):
	# get user
	conn = sqlite3.connect(db)
	query = "SELECT * FROM users WHERE NAME = \"{}\"".format(user)
	df = pd.read_sql_query(query, conn)

	# load in contact list
	contact_json = json.loads(df["contacts"].values[0])
	contact_list = contact_json["contacts"]
	contact_list.append(contact)
	print(contact_list)

	contact_json["contacts"] = contact_list
	print(contact_json)

	# update row
	query = "UPDATE users SET contacts=\'{}\' WHERE NAME=\'{}\';".format(json.dumps(contact_json), user)
	print(query)

	c = conn.cursor()
	c.execute(query)
	conn.commit()
	conn.close()
	return True


def load_all_friends(username):
	# get user
	conn = sqlite3.connect(db)
	query = "SELECT * FROM users WHERE NAME = \"{}\"".format(username)
	df = pd.read_sql_query(query, conn)


	# load in contact list
	contact_json = json.loads(df["contacts"].values[0])
	print(contact_json)
	contact_list = contact_json["contacts"]
	print(contact_list)
	return contact_list


if __name__=="__main__":
	create_user("nick", "nick@speer.ai", "nick6115")

	conn.close()
