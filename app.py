from flask import Flask, redirect, render_template, request, url_for
from flask_bootstrap import Bootstrap
import mongoengine as mongo
from flask_login import (LoginManager, UserMixin, current_user, login_required,
                         login_user, logout_user)


mongo.connect('org_mode')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisupposedtobesecret'
login_manager = LoginManager()
login_manager.init_app(app)
Bootstrap(app)


class User(UserMixin, mongo.Document):
    id = mongo.IntField(unique=True,
                        primary_key=True)
    username = mongo.StringField(unique=True,
                                 max_length=30,
                                 required=True)
    password = mongo.StringField(max_length=30,
                                 required=True)


@login_manager.user_loader
def load_user(user_id):
    # how do i get rid of this function?
    return User.objects(id=user_id).first()


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.objects(username=username)
        if user and user.first().password == password:
            login_user(user.first())
            return redirect(url_for('home'))
        else:
            error = 'Invalid Credentials. Please try again.'

    return render_template('login.html', error=error)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/home')
@login_required
def home():
    return render_template('home.html', username=current_user.username)


if __name__ == '__main__':
    app.run(debug=True)
