from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
from flask_socketio import SocketIO
from database import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

@app.route('/')
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        friends = load_all_friends(session['username'])
        return render_template('friends.html', **locals())

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
    else:
        # login attempt
        status = check_user(request.form['username'], request.form['password'])
        if status == 1:
            session['logged_in'] = True
            session['username'] = request.form['username']
            return index()
        else:
            flash('wrong password!')
            error = "wrong password"
            return render_template('login.html', **locals())


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


@app.route('/chat/<friend>', methods=["GET", "POST"])
def chat_with_friend(friend):
    messages = []

    if request.method == "POST":
        messages.append(request.form["message"])

    return render_template("chat.html", **locals())


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
    socketio.run(app, host='0.0.0.0', debug=True)
