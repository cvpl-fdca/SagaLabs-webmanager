from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from flask import Blueprint, render_template, redirect, url_for, request, g, abort
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from sagalabs.utils.User import User

import json
from functools import wraps
import datetime

# Azure Key Vault

keyVaultUri = "https://sagalabskeyvault.vault.azure.net/"

credential = DefaultAzureCredential()
client = SecretClient(vault_url=keyVaultUri, credential=credential)

secret_name = "SagaLabs-Backbone-Firebase-privatekey-json"
retrieved_secret = client.get_secret(secret_name)

cred_dict = json.loads(retrieved_secret.value)
cred = credentials.Certificate(cred_dict)

# Firebase Service Account
firebase_admin.initialize_app(cred)

bp = Blueprint('sagalabs', __name__, url_prefix='')

# For keeping track of versions
start_time = datetime.datetime.now()

# Useful for creating decorators that enforce a validator wich dependen on its return value continues or returns the return value of not_validated. Examples below declaration
def enforce_requirement(validator, not_validated):
    def x_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if(validator()):
                return f(*args, **kwargs)
            else:
                return not_validated()
        return decorated_function
    return x_required

# This decorator redirects to sagalabs.login if not logged in
login_required = enforce_requirement(lambda: hasattr(g, 'profile_authorized'), lambda: redirect(url_for('sagalabs.login')))
# This decorator aborts with statuscode 401 (Unauthorized) if user is not SuperAdmin
super_admin_required = enforce_requirement(lambda: hasattr(g, 'profile') and g.profile.local_claims["UserType"] == 'SuperAdmin', lambda: abort(401))

# This extract claims from cookie and appends it under the global variable 'g'
@bp.before_request
def validate_cookie():
    cookie = request.cookies.get('sagalabs_auth')
    if cookie:
        try:
            profile = auth.verify_session_cookie(cookie, check_revoked=True)
            user_record = auth.get_user(profile["user_id"])
            user = User(user_record)
            g.profile = user
            g.profile_authorized = True
        #except auth.InvalidSessionCookieError:
        except Exception:
            return
    return

# This sets variables globaly to be used by all templates before render
@bp.context_processor
def inject_value():
    template_variables = {}

    time_since_restart = datetime.datetime.now() - start_time
    time_format_object = {
        'days': time_since_restart.days,
        'hours': time_since_restart.seconds // 3600,
        'minutes': (time_since_restart.seconds % 3600) // 60
    }

    template_variables["run_stamp"] = time_format_object
    if hasattr(g, "profile_authorized"):
        template_variables["profile_authorized"] = g.profile_authorized
        template_variables["profile"] = g.profile
    return template_variables

# Home page
@bp.route('/')
def home():
    return render_template('index.html')

# Labs page
@bp.route('/labs')
@login_required
def labs():
    with open('sagalabs/static/generatedSampleRequest.json', 'r') as sampleFile:
        sampleData = json.load(sampleFile)
        return render_template('labs.html', data=sampleData)


@bp.route('/users')
@login_required
def users():
    # Get a list of users from firebase auth
    userRecordList = auth.list_users().users
    # Creates a user object from userRecordList
    users = list(map(lambda user: User(user), userRecordList))
    return render_template('users.html', users=users)

# This should be removed from production
@bp.route('/PromoteMe', methods=['POST'])
@login_required
def PromoteToSuperAdmin():
    request_url = request.url
    if request_url == "http://127.0.0.1:5000/PromoteMe" or request_url == "http://admindev.sagalabs.dk/PromoteMe":
        claims = g.profile.local_claims
        claims["UserType"] = "SuperAdmin"
        auth.update_user(g.profile.id, custom_claims=claims)
        return '', 200
    else:
        abort(403)
    
@bp.route('/UpdateUserType', methods=['POST'])
@super_admin_required
def UpdateUserType():
    data = request.get_json()
    uid = data.get('uid')
    newType = data.get('UserType')

    # Bad request
    if not newType in ['User', 'Admin', 'SuperAdmin']:
        abort(400)

    # Update user
    user = auth.get_user(uid)
    customClaims = user.custom_claims or {}
    customClaims['UserType'] = newType
    auth.update_user(user.uid, custom_claims=customClaims)
    return '', 200

@bp.route('/login')
def login():
    loging_page = 'https://backbonedev.sagalabs.dk/login?redirect=https://admindev.sagalabs.dk'
    return redirect(loging_page)

@bp.route('/logout')
def logout():
    logout_page = 'https://backbonedev.sagalabs.dk/logout?redirect=https://admindev.sagalabs.dk'
    return redirect(logout_page)