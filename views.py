from flask import Flask
from flask import g, request, redirect, url_for, render_template

from flask.ext.login import LoginManager, current_user, login_user, logout_user
from models import User, initialize_database

app = Flask("TaskList")
app.secret_key = 'super secret key'

login_manager = LoginManager(app)
login_manager.login_view = 'login'


@app.before_request
def before_request():
    g.user = current_user


@login_manager.user_loader
def load_user(id):
    return User.get(id=int(id))


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form['username']
    password = request.form['password']

    registered_user = User.filter(User.username == username).first()

    if registered_user is None:
        return redirect(url_for('login'))  # redirect back to login page if can't wasn't found

    if not registered_user.password.check_password(password):
        return redirect(url_for('login'))  # redirect back to login page if incorrect password

    login_user(registered_user)
    return redirect(request.args.get('next') or url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/registration')
def registration():
    raise NotImplemented()


if __name__ == "__main__":
    initialize_database()
    app.run()