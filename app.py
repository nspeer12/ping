from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
from flask_socketio import SocketIO
from database import create_user

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


if __name__ == '__main__':
    socketio.run(app, debug=True)
