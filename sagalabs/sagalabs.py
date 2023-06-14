from flask import Blueprint, render_template, flash, redirect, url_for, session, request, send_file, abort

import os
import re
import hashlib
from functools import wraps
from base64 import b64encode

from sagalabs.db import get_db

bp = Blueprint('sagalabs', __name__, url_prefix='')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('logged_in') is None:
            flash('Login required', 'error')
            return redirect(url_for('sagalabs.login'))
        return f(*args, **kwargs)
    return decorated_function

# Index page
@bp.route('/')
@login_required
def home():
    return render_template('index.html')

# Login page
@bp.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        # Connect to the database
        db = get_db()

        # Retrieve the users password from database (and check if user exist)
        c = db.execute("SELECT * FROM users WHERE username=?", (request.form['username'],))
        user = c.fetchone()

        # Check if a user was found
        if user is None:
            flash('User not found.', 'error')
            return render_template('login.html')


        if user['password'] != hashlib.sha256(request.form['password'].encode()).hexdigest():
            flash('Invalid password.', 'error')
            return render_template('login.html')


        session['logged_in'] = True
        session['username'] = user['username']
        session['user_id'] = user['id']

        flash('Welcome! You are now logged in.', 'info')

        return redirect(url_for('sagalabs.home'))

    return render_template('login.html')

# Register page
@bp.route('/register', methods=['GET', 'POST'])
def register():

    # for the register to be processed
    if request.method == 'POST':
        usr = request.form['username']
        pwd1 = request.form['password1']
        pwd2 = request.form['password2']
        token = request.form['token']

        db = get_db()
        c = db.cursor()

        #Check if username not provided
        if not len(usr):
            flash('Username not provided', 'error')
            return render_template('register.html')

        # Check length of username
        if len(usr) > 20:
            flash('Username cannot exceed 20 characters', 'error')
            return render_template('register.html')

        # Check if invalid characters
        if not re.fullmatch('[a-zA-Z0-9._]*', usr):
            flash('Username must match [a-zA-Z0-9._]*', 'error')
            return render_template('register.html')

        # Check if username is taken
        c.execute('''SELECT * FROM users WHERE username=? COLLATE NOCASE''', (usr,))
        if c.fetchone() is not None:
            flash(f"Username '{usr}' already taken", 'error')
            return render_template('register.html')

        # Check if the two passwords match
        if pwd1 != pwd2:
            flash('Passwords do not match', 'error')
            return render_template('register.html')

        # Check if password is long enough
        if len(pwd1) < 8:
            flash("Password is too weak, try again.", 'error')
            return render_template('register.html')

        # Check if token is correct
        # admin_key = open('sagalabs/secrets/admin.key', 'r').read()
        admin_key = os.getenv('SL_ADMIN_KEY')
        if admin_key is None:
            print('------ADMIN KEY NOT SET!------')
            admin_key = 's3crEt@dm!n'
        if token != admin_key:
            flash("Admin token is incorrect", 'error')
            return render_template('register.html')

        # If all is well create the user
        hashed_password = hashlib.sha256(pwd1.encode()).hexdigest()

        c.execute("INSERT INTO users (username, password) VALUES (?,?)",
                   (request.form['username'], hashed_password))
        db.commit()

        flash(f"Registration succeeded. You can now log in.", 'info')

        return redirect(url_for('sagalabs.login'))

    # otherwise we return the UI
    return render_template('register.html')


# Logout page
@bp.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('user_id', None)
 
    flash('You are now logged out', 'info')
    return redirect(url_for('sagalabs.login'))