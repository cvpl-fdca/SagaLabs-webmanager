from flask import Blueprint, render_template, flash, redirect, url_for, session, request, send_file, abort

import os
import re
import hashlib
from functools import wraps
import requests
from io import BytesIO
from base64 import b64encode

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

from sagalabs.db import get_db
from sagalabs.users import from_obj

ips = ['http://52.137.44.13', 'http://52.137.43.239', 'http://52.137.44.104','http://52.137.43.174']

bp = Blueprint('sagalabs', __name__, url_prefix='')

def basic_auth():
    with open('sagalabs/secrets/vpn.key', 'r') as f:
        password = f.read()
    token = b64encode(f'sagavpn-api:{password}'.encode()).decode()
    return f'Basic {token}'


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('logged_in') is None:
            flash('Login required', 'error')
            return redirect(url_for('sagalabs.login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin'):
            flash('You are not an admin', 'error')
            return redirect(url_for('sagalabs.home'))
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
        session['admin'] = user['is_admin']

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
        c.execute('''SELECT * FROM users WHERE username=? COLLATE NOCASE''', (usr, ))
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

        # If all is well create the user
        hashed_password = hashlib.sha256(pwd1.encode()).hexdigest()

        # create user with admin privs, if token is correct
        # admin_key = open('sagalabs/secrets/admin.key', 'r').read()
        admin_key = os.getenv('SL_ADMIN_KEY')
        if admin_key is None:
            print('------ADMIN KEY NOT SET!------')
            admin_key = 's3crEt@dm!n'

        token = request.form['token']
        admin = True if token == admin_key else False
        privs = 'Admin' if admin else 'User'

        c.execute("INSERT INTO users (username, password, is_admin) VALUES (?,?,?)",
                   (request.form['username'], hashed_password, admin))
        db.commit()

        flash(f"{privs} '{usr}' registered, you can now log in.", 'info')

        return redirect(url_for('sagalabs.login'))

    # otherwise we return the UI
    return render_template('register.html')


# Logout page
@bp.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('user_id', None)
    session.pop('admin', None)
 
    flash('You are now logged out', 'info')
    return redirect(url_for('sagalabs.login'))


# Temporary pages are used for inspiration and should not reach production:

#enter sagalabs
@bp.route('/enter', methods=['GET'])
@login_required
def enter():
    return render_template('enter.html', lab_count=len(ips) )

#knowledge space
@bp.route('/knowledge', methods=['GET'])
@login_required
def knowledge():
    return render_template('knowledge.html')

#admin panel
@bp.route('/admin', methods=['GET'])
@login_required
@admin_required
def admin():
    user = session.get('username')
    data = {'username': user}
    headers = {'Authorization': basic_auth()}

    # get all users
    try:
        r = requests.post(f'{vpn_url}/api/users/list', headers=headers, data=data, timeout=5) # 1 sec timeout
        r = r.json()
        r = r if r is not None else []

    except:
        abort(503) # service unavailable

    # create array of users, with all their data
    db = get_db()
    c = db.cursor()
    users = []
    for i, user in enumerate(r):
        name = r[i]['Identity']

        # see if users is in db
        c.execute('''SELECT id FROM users WHERE username=? COLLATE NOCASE''', (name, ))
        existing = c.fetchone()
        if existing is not None:
            r[i]['id'] = existing['id']

        users.append(from_obj(r[i]))

    user_count = len(users)
    connected = len([u for u in users if u.connected])

    return render_template('admin.html', users=users, count=user_count, connected=connected)

# Delete user
@bp.route('/delete/<user>', methods=['GET'])
@login_required
@admin_required
def delete_user(user):
    data = {'username': user}
    headers = {'Authorization': basic_auth()}

    try:
        # revoke the key
        r = requests.post(f'{vpn_url}/api/user/revoke', headers=headers, data=data, timeout=1.0)
    except:
        abort(503)

    if not r.ok:
        flash('Something went wrong trying to revoke the key', 'error')
        return redirect(url_for('sagalabs.enter'))

    try:
        # delete the key
        r = requests.post(f'{vpn_url}/api/user/delete', headers=headers, data=data, timeout=1.0)
    except:
        abort(503)

    if not r.ok:
        flash('Something went wrong trying to delete the user', 'error')
        return redirect(url_for('sagalabs.enter'))

    flash('User deleted successfully', 'info')
    return redirect(url_for('sagalabs.admin'))

# Download
@bp.route('/download/<int:num>', methods=['GET'])
@login_required
def download_config(num):
    try:
        url = ips[num-1] # visually 1-n
    except:
        abort(400)

    user = session.get('username')
    data = {'username': user}
    headers = {'Authorization': basic_auth()}

    try:
        ## create key, if not already existing
        r = requests.post(f'{url}/api/user/create', headers=headers, data=data, timeout=1.0)

        # get the key, newly created or not
        r = requests.post(f'{url}/api/user/config/show', headers=headers, data=data, timeout=1.0)

    except:
        abort(503)

    # write the file to a buffer
    buffer = BytesIO()
    buffer.write(r.content)
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name=f'{user}_lab{num}.ovpn', mimetype='text/csv')
