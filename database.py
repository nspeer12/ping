import sqlite3
import pandas as pd

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
	password = hash(password)

	c = conn.cursor()
	c.execute("INSERT INTO users VALUES ( \'{}\', \'{}\',\'{}\', \'{}\');".format(ID, email, name, password))
	print("inserted user")
	conn.commit()
	conn.close()

	return "registration successful!"


if __name__=="__main__":
	create_user("nick", "nick@speer.ai", "nick6115")

	conn.close()
