from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
from flask_socketio import SocketIO
from database import create_user, list_users, add_contact

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

@app.route('/')
def sessions():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('session.html', **locals())

def messageReceived(methods=['GET', 'POST']):
	print('message was received')

@socketio.on('chat created')
def handle_my_custom_event(json, methods=['GET', 'POST']):
	print('received my event: ' + str(json))
	socketio.emit('my response', json, callback=messageReceived)


@app.route('/logout', methods=["POST", "GET"])
def logout():
    session['logged_in'] = False
    session['username'] = None
    return render_template("logout.html")

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template('login.html')

    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
        session['username'] = request.form['username']
        return sessions()
    else:
        flash('wrong password!')
        return

@app.route('/register', methods=["POST", "GET"])
def register():
    return render_template("register.html")

@app.route('/register_user', methods=["POST", "GET"])
def register_user():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    res = create_user(username, email, password)
    if res != "registration successful!":
        error = res
        return render_template('register.html', **locals())


    session['logged_in'] = True
    session['username'] = request.form['username']
    return sessions()



@app.route('/add_contact', methods=["POST"])
def add_friend():
    add_contact(session["username"], request.form["user"])
    return render_template("find_contacts.html")

@app.route('/find_contacts', methods=["POST", "GET"])
def find_contacts():
    # if user makes a request
    if request.method == "POST":
        search = request.form["username"]
        users = list_users(search)
    else:
        # load in every contact from database
        users = list_users()

    userlen = len(users)
    return render_template("find_contacts.html", **locals())


if __name__ == '__main__':
    socketio.run(app, debug=True)
