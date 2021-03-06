from flask import render_template, redirect, session, request, flash
from flask_app import app

from flask_app.models.user import User
from flask_bcrypt import Bcrypt
import hashlib
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def signup():
    if 'user_id' in session:
        return redirect('/topics')
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():

    if not User.validate_register(request.form):
        return redirect('/register')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "email_hash": hashlib.md5((request.form['email']).strip().lower().encode('utf-8')).hexdigest(),
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    session['user_id'] = User.add(data)

    return redirect('/topics')

@app.route('/login')
def instructor_login():
    if 'user_id' in session:
        return redirect('/topics')
    return render_template('login.html')

@app.route('/login',methods=['POST'])
def login():
    user = User.get_by_email(request.form)

    if not user:
        flash("Invalid login credentials","login")
        return redirect('/login')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid login credentials","login")
        return redirect('/login')
    session['user_id'] = user.id
    return redirect('/topics')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')